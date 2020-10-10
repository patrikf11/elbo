const thingsSpeakProps = { 
    fields : {
        V:"field1",
        I:"field2",
        STATUS:"field3",
        PV:"field4",
        PPV:"field5",
        YIELDTODAY:"field6",
        YIELDTOTAL:"field7",
        TEMP:"field8"
    },
    feedUrl:"https://api.thingspeak.com/channels/1095413/feeds.json?results=800",
    histUrl:"./preprocess/hist.json"
};

const props={
    colors:{
        OFF:"#dcdcdc", //#f6f6f6"
        OFF1:"#dcdcdc",//f6f6f6"
        ERR:"#eb3434",
        BULK:"#add8e6", //"lightblue"
        ABS:"#ffd995",
        FLOAT:"#90ee90" //"lightgreen"
    },
    labels:{
        OFF:"Off", 
        OFF1:"Off",
        ERR:"Err",
        BULK:"Bulk",
        ABS:"Abs",
        FLOAT:"Float", 
        MEDIAN:"Median"
    },
};

