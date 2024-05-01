

const percentageFormatter = (value, ctx, displayType) =>{
    if(displayType === 'number'){
        return value
    }
    let sum = 0;
    let dataArr = ctx.chart.data.datasets[0].data;
    dataArr.map(data => {
        if(data < 0) return;
        sum += data;
    });
    if(value === 0 || value < 0){
        return ''
    }
    return (value*100 / sum).toFixed(0)+"%";
}

const pieChartOffsetFormatter = (context) => {
    let value = context.chart.data.datasets[0].data[context.dataIndex]
      let sum = 0;
      let dataArr = context.chart.data.datasets[0].data;
      dataArr.map(data => {
          sum += data;
      });
      let percentage = (value*100 / sum).toFixed(0);

      if(percentage <= 10){
        return 20
      }else if(percentage > 10 && percentage < 20){
        return 10
      }
        return -20;
}

export { percentageFormatter, pieChartOffsetFormatter }