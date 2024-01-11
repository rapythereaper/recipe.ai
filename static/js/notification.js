// import sweet lert first
var MEAL=localStorage.getItem("meal_notification");
var INVENTORY=localStorage.getItem("inventory");

if(MEAL)MEAL=JSON.parse(MEAL);
if(INVENTORY)INVENTORY=INVENTORY.parse(INVENTORY);



const ALERT_SOUND=new Audio("/static/music/alert.mp3")

function calculateTimeDifference(givenTimeString) {
    // Parse the given time string into hours and minutes
    const [givenHours, givenMinutes] = givenTimeString.split(':').map(Number);

    // Get the current time
    const currentTime = new Date();
    const currentHours = currentTime.getHours();
    const currentMinutes = currentTime.getMinutes();

    // Calculate the time difference in seconds
    const timeDifferenceInSeconds = (givenHours - currentHours) * 3600 + (givenMinutes - currentMinutes) * 60;

    return timeDifferenceInSeconds;
}

function isNotified(meal){
    if(!MEAL) return false;
    for(let i of MEAL){
       
        if(i.id===meal.id && i.time==meal.time && i.food==meal.food){
            if(! i.isNotified) return false;
            return true;
        }
    }
    return false
}

function setNotified(meal,status=true){
    if(!MEAL)MEAL=[]
    for(let i of MEAL){
        if(i.id===meal.id){
            i.id=meal.id;i.time=meal.time;i.food=meal.food;
            i.isNotified=status;
            return
        }
    }
    meal.isNotified=status
    MEAL.push(meal)
}
function saveState(name,data){
    localStorage.setItem(name, JSON.stringify(data));
}

async function getNotification(){
    let res=await fetch("/api/notification");
    let notification=await res.json();
    console.log(notification)
    for(let i of notification.meal_plan){
        let msg=i.food
        let id=i.id;
        let time=calculateTimeDifference(i.time)
        console.log("Notification in "+time+"s");
        if(time<0 || isNotified(i)) continue;
        console.log("Notification in "+time+"s");
        setNotified(i,true)
        const myTimeout = setTimeout(async()=>{
            ALERT_SOUND.play()
            Swal.fire({
                title: "Meal Alert?",
                text: `Time to eat ${msg}`,
                icon: "info"
              });
            saveState("meal_notification",MEAL)
            
        }, 1000*time)
    }
    
}

setTimeout(getNotification,1000*3)