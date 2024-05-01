<template>
  <stackedbarchart :chart-options="options" :chart-data="chartData" :style="style">

  </stackedbarchart>
</template>

<script>
import stackedbarchart from "@/components/charts/stackedbarchart";
import { chartLegendDynamic } from "@/helpers/chartStyle";

export default {

  name: 'ageGenderChart',
  components: { stackedbarchart },
  emits: ['loaded', 'startLoading', 'noData'],
  methods: {
    load(promise) {
      this.loaded = false;
      this.$emit('startLoading')
      promise.then((response) => {
        console.log('response', response.data);
        this.chartData = response.data
        // let data = response.data;
        if (this.allAreZero(response.data.female) && this.allAreZero(response.data.male)) {
          this.noData = true;
          this.data.datasets[0].data = this.dummiData.female
          this.data.datasets[1].data = this.dummiData.male
          this.$emit('noData')
        } else {
          this.noData = false;
          this.data.datasets[0].data = response.data.female
          this.data.datasets[1].data = response.data.male
          this.data.datasets[2].data = response.data.max
        }
        this.loaded = true;
        this.$emit('loaded')
      })
    },
    allAreZero(arr) {
      return arr.every(element => element === 0);
    }
  },
  data: (scope) => ({
    noData: false,
    dummiData: { "male": [1, 1, 1, 1, 1], "female": [1, 1, 1, 1, 1] },
    style: {
      height: "400px"
    },
    loaded: false,
    options: {
      indexAxis: 'y',
      responsive: true, maintainAspectRatio: false,
      barThickness: 50,
      layout: {
        padding: 0
      },
      plugins: {
        legend: chartLegendDynamic(scope)

      },
      scales: {

        x: {

          stacked: true,
          grid: {
            display: false,
            drawBorder: false,
          },
          ticks: {
            display: false
          },
          offset: 0,

        },
        y: {
          stacked: true,
          grid: {
            display: false,
            drawBorder: false
          },
          ticks: {
            display: false
          },
          offset: 50,
        }
      },
      borderColor: '#EDF5F7',
      borderSkipped: false,
      borderWidth: 4,
      borderRadius: { topLeft: 10, topRight: 10, bottomLeft: 10, bottomRight: 10 },
    },
    data: {
      labels: ['< 18 ' + scope.$t('year'), '18 - 25', '26 - 35', '36 - 45', '46+'],
      datasets: [
        {
          label: scope.$t('Female'),
          data: [],
          backgroundColor: '#E9828C',
          datalabels: {
            align: 'end',
            anchor: 'start',
            color: '#fff',
            labels: {
              title: {
                font: {
                  weight: 'bold',
                  size: '12'
                }
              }
            },
            formatter: function (value, context) {
              let dataIndex = context.dataIndex;
              switch (dataIndex) {
                case 0:
                  return '< 18 ' + scope.$t('year')
                case 1:
                  return '18 - 25'
                case 2:
                  return '26 - 35'
                case 3:
                  return '36 - 45'
                case 4:
                  return '46+'
              }
              return 'oops'

            },
          }
        }, {
          label: scope.$t('Male'),
          data: [],
          backgroundColor: '#90D5E9',
          datalabels: {
            display: false,
            align: 'right',
            labels: {
              title: {
                font: {
                  weight: 'bold',
                  size: '12'
                }
              }
            }

          }
        },
        {
          label: '',
          data: [],
          backgroundColor: '#d9f0f7',
          datalabels: {
            color: '#000',
            anchor: 'end',
            formatter: function (value, context) {
              let female = context.chart.data.datasets[0].data[context.dataIndex];
              let male = context.chart.data.datasets[1].data[context.dataIndex];
              if (female + male == 0) {
                return '0'
              }
              else {
                return female + male;
              }
            },
            align: 'right',
            labels: {
              title: {
                font: {
                  weight: 'bold',
                  size: '12'
                }
              }
            }
          }
        }
      ]
    },
    chartData:{}
  })

}
</script>