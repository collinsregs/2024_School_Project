const playwright = require("playwright")
const fs = require('fs').promises;
const logger = require("./logger");
const schedule = require ("node-schedule")


const addPageInterceptors = async (page)=>{
    await page.route("**/*", (route)=>{
        const request = route.request();
        const resourceType = request.resourceType();
        if(
            resourceType === "image"||
            resourceType === "font"||
            resourceType === "stylesheet"||
            resourceType === "script"||
            resourceType === "media"
        ){
            route.abort();
        }else{
            route.continue()
        }
    });
};
const getAttribute = async (handle)=>{
return handle.evaluate((element)=>{
const attributeMap={};
for (const attr of element.attributes){
    attributeMap[attr.name]=attr.value;
};
return attributeMap;
});
};
async function parseComment(e){
    const things = await e.$$("> .sitetable > .thing");
    let comments =[];
    for (const thing of things){
        let thingsClass = await things[0].getAttribute("class");
        let children = await parseComment(await thing.$(".child"));
        let isDeleted = thingsClass.includes("deleted");
        const mdDiv = await thing.$("div.md");
        let comment= ""
        if (mdDiv){
        comment= isDeleted ?"" :await thing.$eval("div.md",(el)=> el.innerText.trim());
        }
        const spanScore = await thing.$("span.score")
        let points = ''
        if (spanScore){
        points= isDeleted?"":await thing.$eval("span.score",(el)=>el.innerText.trim());
        }
        comments.push({comment,points,children,isDeleted});
    }
    return comments;
}
async function getPostData({page,post}){
    logger.info("getting details for post", { post: post.id });
    await page.goto(post.url,{timeout: 0});
    const sitetable = await page.$("div.sitetable");
    const thing = await sitetable.$(".thing");
    let id= post.id;
    let subreddit = post.subreddit;
    const attributes = await getAttribute(thing);
    let dataType = attributes["data-type"];
    let dataUrl = attributes["data-url"];
  let title = await page.$eval("a.title", (el) => el.innerText);
  let points = parseInt(await sitetable.$(".score.unvoted").innerText);
  let text = await sitetable.$("div.usertext-body").innerText;
    let comments = await parseComment(await page.$("div.commentarea"));
    return{id, subreddit, dataType, dataUrl, title, points, text, comments};
}
async function getPostOnPage(page){
    const elements= await page.$$(".thing");
    let posts= [];
    for(const element of elements){
        const attributes = await getAttribute(element);
        const id = attributes["data-fullname"];
        const subreddit = attributes["data-subreddit-prefixed"];
        const time = attributes["data-timestamp"];
        const timestamp = parseInt(time);
        const url = `https://old.reddit.com${attributes["data-permalink"]}`;
        posts.push({id,subreddit,timestamp,url})
    }
    return posts;
}
// main function 
async function main(subreddit){
// creating browser and browser object
    const browser = await playwright.chromium.launch({
        headless: false,
        proxy:{server:'http://localhost:8888'}
    });
    const context = await browser.newContext({ 
        UserAgent:'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
       });
    const page = await context.newPage();
    addPageInterceptors(page);
// getting page object
    await page.goto(`https://old.reddit.com/r/${subreddit}/new/`,{timeout : 0});
    let hour = 1000 * 60 *60;
    let now = Date.now();
    let cutoff = Date.now() - 24 * hour;
    let earliest = new Date();
    let posts = [];
    while (cutoff< earliest){
// getting posts from page
        let pagePosts = await getPostOnPage(page);
        if(pagePosts.length ==0 ){
            logger.warn("breaking no posts on page")
            break;
        }
        posts = posts.concat(pagePosts);
        let earliestPost = posts[posts.length-1];
        earliest= earliestPost.timestamp;

        if(earliestPost<cutoff){
            break;
        }
        let nextPageUrl= await page.$eval(".next-button a",(el)=>el.href);
        await page.goto(nextPageUrl);
    }
    posts= posts.filter((post)=> post.timestamp>cutoff);
    let data = []
     for(const post of posts){
        let postData = await getPostData({post, page});
        data.push(postData)
     }
     let filename = now +"_"+ subreddit
     try{
    await fs.writeFile(`./Data/${filename}.json`,JSON.stringify(data,null,2),'utf-8');
    logger.info(`successfully wrote to ${filename}`)
     }catch(err){
        logger.error(`Error writing to ${filename}`, err)
     }
    await browser.close();
}
async function run (subreddit_list){
    for(sub of subreddit_list){
        logger.info(`getting reddit posts for the subreddit :${sub}`);
        await main(sub);
    }
}
if (require.main===module){
    let subreddit_list = ['Technology', 'Tech', 'TechNews','Gadgets', 'TechSupport','Coding', 'Programming', 'webdev', 'cybersecurity','artificial', 'futurology']

    // schedule.scheduleJob('0 2 * * *', function(){
    run(subreddit_list);
    // })

}
