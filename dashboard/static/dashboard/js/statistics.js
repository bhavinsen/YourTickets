$(function() {

    $('.dropdown-event-selector').hide();
    $('.dropdown-event-selector').select2();
    $('.dropdown-date_range-selector').select2({ minimumResultsForSearch : -1 });

    var chart_revenue;

    function createChart(tickets, labels, revenue, compare_revenue, compare_tickets, event_names){
        var bar_max = 45 + 10;
        var line_max = 1 + 10;

        if(chart_revenue){
            chart_revenue.destroy();
        }

        var revenue_chart_data = {
            labels: labels,
            datasets: [{
                type: 'line',
                label: event_names.event+', ticketsold',
                borderColor: '#5c93e0',
                backgroundColor: '#55c7e0',
                fill: false,
                yAxisID: 'y-axis-tickets',
                borderDash: [5, 5], //length and spacing
                //the point
                pointBorderWidth: 2,
                pointBorderColor: '#5c93e0',
                pointRadius: 3,
                pointBackgroundColor: '#FFFFFF',
                data: tickets
            }, {
                type: 'bar',
                label: event_names.event+', revenue',
                borderColor: '#55c7e0',
                backgroundColor: '#55c7e0',
                fill: false,
                yAxisID: 'y-axis-revenue',

                data: revenue
            }]
        };

        if(compare_revenue.length > 0){
            revenue_chart_data.datasets.push({
                type: 'line',
                label: event_names.compare_event+', ticketsold',
                borderColor: '#912837',
                backgroundColor: '#D7283C',
                fill: false,
                yAxisID: 'y-axis-tickets',
                borderDash: [5, 5], //length and spacing
                //the point
                pointBorderWidth: 2,
                pointBorderColor: '#912837',
                pointRadius: 3,
                pointBackgroundColor: '#FFFFFF',
                data: compare_tickets
            });

            revenue_chart_data.datasets.push({
                type: 'bar',
                label: event_names.compare_event+', revenue',
                borderColor: '#D7283C',
                backgroundColor: '#D7283C',
                fill: false,
                yAxisID: 'y-axis-revenue',

                data: compare_revenue
            });

        }

        var ctx = document.getElementById('chart-revenue').getContext('2d');

        chart_revenue = new Chart(ctx, {
            type: 'bar',
            data: revenue_chart_data,
            options: {
                maintainAspectRatio: false,
                responsive: true,
                hoverMode: 'index',
                // stacked: false,
                title: {
                    display: true,
                    text: 'Tickets en Revenue'
                },
                tooltips: {
                    mode: 'index',
                    axis: 'y'
                },
                scales: {
                    yAxes: [{
                        label: 'Aantal verkochte Tickets',
                        // type: 'linear', // only linear but allow scale type registration. This allows extensions to exist solely for log scale for instance
                        display: true,
                        position: 'left',
                        id: 'y-axis-tickets',
                        ticks: {
                            beginAtZero: true,
                            suggestedMax: line_max
                        }
                    }, {
                        label: 'Omzet',
                        // type: 'linear', // only linear but allow scale type registration. This allows extensions to exist solely for log scale for instance
                        display: true,
                        position: 'right',
                        id: 'y-axis-revenue',
                        ticks: {
                            beginAtZero: true,
                            suggestedMax: bar_max
                        },
                        // grid line settings
                        gridLines: {
                            drawOnChartArea: false, // only want the grid lines for one axis to show up
                        }
                    }]
                }
            }
        });
    }

    function getUrlParams(){
        var url = '';

        var event_value = $('.dropdown-event-selector').val();
        var date_value = $('.dropdown-date_range-selector').val();

        if(event_value !== '0'){
            url += 'compare_to='+event_value+'&';
        }
        url += 'date='+date_value;

        return url;
    }

    function loadChart() {
        YT.showLoader($('#chart-revenue-container'), null, '/static/dashboard/img/loader_dashboard.gif')

        var url = $('#chart-revenue').data('url');



        var event_names = {
            'event': $('#chart-revenue').data('event_name'),
            'compare_event': ''
        };

        if($('.dropdown-event-selector').select2('data')[0].id !== '0'){

            event_names['compare_event'] = $('.dropdown-event-selector').select2('data')[0].text;
        }

        // if(compare_event_id){
        //     url +='?compare_to='+compare_event_id
        // }
        url += '?'+getUrlParams();

        $.ajax({
            url: url,
            method: "get",
            success: function (data) {
                YT.hideLoader($('#chart-revenue-container'))
                if(data.success){
                    createChart(data.tickets, data.labels, data.revenue, data.compare_revenue, data.compare_tickets, event_names)
                    $('.dropdown-event-selector').show();
                }

            }
        });
    }

    loadChart();

    $('.dropdown-event-selector').on('select2:select', function(e){
        loadChart();
    });

    $('.dropdown-date_range-selector').on('select2:select', function(e){
        loadChart();
    })

});

// let HttpDataLoader = {
//     install: function(Vue, options){
//         Vue.prototype.loadData = function(){
//             console.log('menb')
//         }
//         // Vue.prototype.$test = '=========llleeeegggg';
//         Vue.prototype.beforeMount = function(){
//             console.log('sdfdasfdfafsdf')
//         }
//
//         Vue.data = function(){
//             console.log('data ===')
//             return {
//                 url: 'url from plugin'
//             }
//         }
//
//     }
// };

// Vue.use(HttpDataLoader);

Vue.mixin({
    data: function(){
        return {
            httpUrl: '',
            httpData:{}
        }
    },
    created: function(){
        if(this.$attrs.hasOwnProperty('http-url')){
            this.httpUrl = this.$attrs['http-url'];
        }
        if(this.httpUrl !== '' && this.httpUrl !== undefined){
            this.$loadHttpData(this.httpUrl);
        }
    },
    // watch:{
    //     httpUrl: function(){
    //         this.$loadHttpData(this.httpUrl)
    //     }
    // },
    methods: {
        $loadHttpData: function(url){

            url = url || this.httpUrl;
            console.log('load')
            let prom = new Promise(
                function(resolve, reject){
                    this.$http.get(url).then(
                        function(res) {
                            this.httpData = res.body;

                            resolve(res.body);
                        }.bind(this)
                    );

                }.bind(this)
            );
            prom.then(this.$httpCallback)
        },
        $httpCallback:function(data){}
    }
});

Vue.component('sales-data-table', {
    props:[],
    template: '#sales-data-table-template',
    data: function(){
        return {
            httpUrl: '',
            httpData:{
                'labels':[]
            },
            items: [
              { message: 'Foo' },
              { message: 'Bar' }
            ]
        }
    },

    created: function(){
        // console.log('=====')
        // this.loadData();
        // console.log(this.httpData)
        // this.httpData()
        // this.$loadHttpData('asdf')
        // this.$loadHttpData(self.getUrl());

    },
    mounted: function(){
        var self = this;
        $('.dropdown-event-selector').on('select2:select', function(e){
            console.log('triggered')
            self.$loadHttpData(self.getUrl());
        });
    },
    methods: {
        $httpCallback:function(data){
            //sold ticket

            console.log('===== data loaded')
        },

        test: function() {
            console.log(this.httpData)
        },
        getUrl:function(){
            var url = this.httpUrl;
            url += "?" + this.getUrlParams();

            return url;
        },
        getUrlParams: function (){
            var url = '';

            var event_value = $('.dropdown-event-selector').val();
            var date_value = $('.dropdown-date_range-selector').val();

            if(event_value !== '0'){
                url += 'compare_to='+event_value+'&';
            }
            url += 'date='+date_value;

            return url;
        }
    },
    watch: {
        httpData:function(value){
            console.log('it changed')
        }
    }


});

