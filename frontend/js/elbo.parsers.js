
function parseHist(data, props){
    var dsOff=[],dsBulk=[],dsAbs=[],dsFloat=[],dsMedian=[],
        startIdx=data.length-29,dt,
        COLOR=props.colors,
        LABEL=props.labels;
        
    $.each(data, function(idx,val){
        dt=val.dt;
        var minV=val.minV/1000,
            div0=val.div0/1000,
            div3=val.div3/1000,
            div4=val.div4/1000,
            div5=val.div5/1000;
        if ( idx>startIdx && minV>5){	
        dsOff.push([dt,minV,minV]);
        if (div0 > minV) dsOff.push([dt,div0,minV]);
        dsBulk.push([dt,div0,div0]);
        if (div3 > div0) dsBulk.push([dt,div3,div0]);
        dsAbs.push([dt,div3,div3]);
        if (div4 > div3) dsAbs.push([dt,div4,div3]);
        dsFloat.push([dt,div4,div4]);
        if (div5 > div4) dsFloat.push([dt,div5,div4]);
        dsMedian.push([dt+43000000,val.medianV/1000])
        }
    });
    var barSets = function(label,data,color){
            return {label:label, data:data, 
                    color:lightenDarkenColor(color,-75), 
                    bars: {show: true, lineWidth:3, fill:true,fillColor:color}
                      };
        },
        lineOpts={show: true,lineWidth:3, fill:false};
    return [barSets(LABEL.OFF, dsOff, COLOR.OFF),
            barSets(LABEL.BULK, dsBulk, COLOR.BULK),
            barSets(LABEL.ABS, dsAbs, COLOR.ABS),
            barSets(LABEL.FLOAT, dsFloat, COLOR.FLOAT),
            {label:LABEL.MEDIAN, data:dsMedian, lines: lineOpts}
        ]	
}
