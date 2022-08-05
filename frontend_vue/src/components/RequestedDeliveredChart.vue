var option = {
  dataset: {
    source: [
      ['score', 'amount', 'product'],
      [100, 90, '2010'],
      [70, 152, '2011'],
      [60, 90, '2012'],
      [50, 100, '2013'],
    ]
  },
  xAxis: {type: 'category'},
  yAxis: {},
  series: [
    {
      type: 'bar',
      barWidth: 10,
      itemStyle: {
        borderRadius: 5,
        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
          { offset: 0, color: '#14c8d4' },
          { offset: 1, color: '#43eec6' }
        ])
      },
      encode: {
        // Map "amount" column to x-axis.
        x: 'product',
        // Map "product" row to y-axis.
        y: 'amount'
      }
    },
        {
      type: 'bar',
       barGap: '-100%',
      barWidth: 10,
      itemStyle: {
        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
          { offset: 0, color: 'rgba(20,200,212,0.5)' },
          { offset: 0.2, color: 'rgba(20,200,212,0.2)' },
          { offset: 1, color: 'rgba(20,200,212,0)' }
        ])
      },
      z: -12,
      encode: {
        // Map "amount" column to x-axis.
        x: 'product',
        // Map "product" row to y-axis.
        y: 'score'
      }
    }
  ]
};
