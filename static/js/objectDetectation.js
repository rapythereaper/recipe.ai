var MODEL;
roboflow.auth({
    publishable_key: "rf_FLtVeRND9PTuFgUnsDU5tqx3aFy2"
}).load({
    model: "food-detection-isnlw",
    version: 1 // <--- YOUR VERSION NUMBER
}).then(function(model) {
    MODEL=model
});

async function predict(el,input_el,canvas_el){
    if(!MODEL)return;
    let data=await MODEL.detect(el);
    console.log(data)
    if(!data){
        alert("Sorry notthing detected in Image try again!")
        return;
    }
    for(let i of data){
        const ctx = canvas_el.getContext("2d");
        ctx.canvas.width  = el.width;
        ctx.canvas.height = el.height
        ctx.drawImage(el, 0, 0);
        ctx.beginPath();
        ctx.rect(i.bbox.x, i.bbox.y, i.bbox.width, i.bbox.height);
        //Fill(i.color)
        ctx.stroke()

    }
}