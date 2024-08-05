const fs = require('fs')
const path = require('path')
const cleanData = require("./stripping")

let reddit_dir = "C:\\Users\\colli\\OneDrive\\Documents\\_projects\\_temp_data_cleaning\\_temp_reddit\\Data\\";
let staging_dir = "C:\\Users\\colli\\OneDrive\\Documents\\_projects\\_temp_data_cleaning\\Staging\\";
let heap_dir = "C:\\Users\\colli\\OneDrive\\Documents\\_projects\\_temp_data_cleaning\\Heap\\";
let data_dir = "C:\\Users\\colli\\OneDrive\\Documents\\_projects\\_temp_data_cleaning\\Data\\"


async function moveFiles(old_dir,new_dir,file){
    let old_path = path.join(old_dir,file)
    let new_path = path.join(new_dir,file)
    await fs.renameSync(old_path,new_path,function(err){
        if(err)throw err
    })
}
function movDataReddit(){
    console.log("moving data to staging")
fs.readdir(reddit_dir,(err,files)=>{
    if(err)throw err;
    for(let file of files){
      moveFiles(reddit_dir,staging_dir,file)
    }
    cleanFromStaging()
})}



function cleanFromStaging(){
    console.log("cleaning staging data")
    fs.readdir(staging_dir,(err,files)=>{
        if(err)throw err
        for(let file of files){
            let file_path = path.join(staging_dir,file)
            let clean=cleanData(file_path)
            let filename = data_dir+file
            fs.writeFile(filename, JSON.stringify(clean),(err)=>{
                if(err) throw err;
                console.log("moving files to heap")
                moveFiles(staging_dir,heap_dir,file)
            })
        }
    })
}

movDataReddit()

