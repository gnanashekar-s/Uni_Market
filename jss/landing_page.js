const slides = document.querySelectorAll(".slider");
var counter =0;

var no_of_images = 0;
slides.forEach(
    (slide,index)=>{
        no_of_images++
        slide.style.left = String(index*100)+'%';

        console.log(no_of_images)
    }
)
const goPrev = ()=>{
    if(counter<=((no_of_images-1)*-1)){
        counter=1;
    }
    counter--
    console.log(counter)
    slideImage()
}
const goNext = ()=>{
    if(counter>=0){
        counter = (no_of_images)*-1
    }
        counter++
        console.log(counter)
        slideImage()
}


const slideImage = () => {
    slides.forEach(
        (slide)=>{
            slide.style.transform = 'translateX'+'('+String(counter*100)+'%'+')'
        }
    )
}
const auto = ()=>{
    while(true){
        setTimeout(
            goNext()
          ,10000)
    }
}
