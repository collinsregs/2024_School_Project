function cleanData(filePath){
let data = require(filePath)
let cleaned_data  = []


for( let index in data){
    let text =[]
    let points =0 
    let item = data[index]
    let title= item.title
    let result = getComments(item)

    text= text.concat(title)
    text= text.concat(result.comments)
    if(item.points!=null){
        points += getPoints(item)
    }
    points+=result.points
    cleaned_data.push({text, points})
}
return cleaned_data}


function getComments(item){
    let list = [];
    let points = 0;
    
    if (item.comments && Array.isArray(item.comments) && item.comments.length != 0){
        for(let index in item.comments){
            let comment = item.comments[index].comment.replace(/\n/g,'');
            list.push(comment);
            points += getPoints(item.comments[index]);
            if(item.comments[index].children && Array.isArray(item.comments[index].children) && item.comments[index].children.length != 0){
                for(let childIndex in item.comments[index].children){
                    let childResult = getComments(item.comments[index].children[childIndex]);
                    list = list.concat(childResult.comments);
                    points += childResult.points;
                }
            }
        }
    }
    return {comments: list, points: points};
}
function getPoints(item){
    if (item.points!=null){
        return Number(item.points.replace(/[^0-9]/g,''))
    }else{
        return 0
    }
}

module.exports = cleanData
