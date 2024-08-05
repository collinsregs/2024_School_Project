"use strict";

var randomChartData = function randomChartData(n) {
  var data = [];
  for (var i = 0; i < n; i++) {
    data.push(Math.round(Math.random() * 200));
  }
  return data;
};
var chartColors = {
  "default": {
    primary: '#FF00FF',
    info: '#00FF00',
    danger: '#00FFFF',
    warning: '#FFFF00',
    success: '#FFA500'
  }
};
var ctx = document.getElementById('big-line-chart').getContext('2d');
new Chart(ctx, {
  type: 'line',
  data: {
    datasets: [{
      fill: false,
      borderColor: chartColors["default"].primary,
      borderWidth: 2,
      borderDash: [],
      borderDashOffset: 0.0,
      pointBackgroundColor: chartColors["default"].primary,
      pointBorderColor: 'rgba(255,255,255,0)',
      pointHoverBackgroundColor: chartColors["default"].primary,
      pointBorderWidth: 20,
      pointHoverRadius: 4,
      pointHoverBorderWidth: 15,
      pointRadius: 4,
      data: [724, 628, 411, 249, 82, 650, 554, 478, 427],
      label: 'intrusion detection systems (IDS)'
    }, {
      fill: false,
      borderColor: chartColors["default"].info,
      borderWidth: 2,
      borderDash: [],
      borderDashOffset: 0.0,
      pointBackgroundColor: chartColors["default"].info,
      pointBorderColor: 'rgba(255,255,255,0)',
      pointHoverBackgroundColor: chartColors["default"].info,
      pointBorderWidth: 20,
      pointHoverRadius: 4,
      pointHoverBorderWidth: 15,
      pointRadius: 4,
      data: [754, 633, 408, 250, 81, 604, 427, 382, 407],
      label: 'data warehousing'
    }, {
      fill: false,
      borderColor: chartColors["default"].danger,
      borderWidth: 2,
      borderDash: [],
      borderDashOffset: 0.0,
      pointBackgroundColor: chartColors["default"].danger,
      pointBorderColor: 'rgba(255,255,255,0)',
      pointHoverBackgroundColor: chartColors["default"].danger,
      pointBorderWidth: 20,
      pointHoverRadius: 4,
      pointHoverBorderWidth: 15,
      pointRadius: 4,
      data: [769, 422, 50, 712, 149, 895, 363, 541, 449],
      label: 'nanotechnology'
    }, {
      fill: false,
      borderColor: chartColors["default"].warning,
      borderWidth: 2,
      borderDash: [],
      borderDashOffset: 0.0,
      pointBackgroundColor: chartColors["default"].warning,
      pointBorderColor: 'rgba(255,255,255,0)',
      pointHoverBackgroundColor: chartColors["default"].warning,
      pointBorderWidth: 20,
      pointHoverRadius: 4,
      pointHoverBorderWidth: 15,
      pointRadius: 4,
      data: [702, 778, 599, 433, 247, 613, 88, 616, 554],
      label: 'input devices'
    }, {
      fill: false,
      borderColor: chartColors["default"].success,
      borderWidth: 2,
      borderDash: [],
      borderDashOffset: 0.0,
      pointBackgroundColor: chartColors["default"].success,
      pointBorderColor: 'rgba(255,255,255,0)',
      pointHoverBackgroundColor: chartColors["default"].success,
      pointBorderWidth: 20,
      pointHoverRadius: 4,
      pointHoverBorderWidth: 15,
      pointRadius: 4,
      data: [995, 873, 729, 602, 548, 759, 832, 917, 982],
      label: 'electrical engineering'
    }],
    labels: ['2024-02-15', '2024-02-22', '2024-02-29', '2024-03-06', '2024-03-13', '2024-03-20', '2024-03-27', '2024-04-03', '2024-04-10']
  },
  options: {
    maintainAspectRatio: false,
    legend: {
      display: true
    },
    responsive: true,
    tooltips: {
      backgroundColor: '#f5f5f5',
      titleFontColor: '#333',
      bodyFontColor: '#666',
      bodySpacing: 4,
      xPadding: 12,
      mode: 'nearest',
      intersect: 0,
      position: 'nearest'
    },
    scales: {
      yAxes: [{
        barPercentage: 1.6,
        gridLines: {
          drawBorder: false,
          color: 'rgba(29,140,248,0.0)',
          zeroLineColor: 'transparent'
        },
        ticks: {
          padding: 20,
          fontColor: '#9a9a9a'
        }
      }],
      xAxes: [{
        barPercentage: 1.6,
        gridLines: {
          drawBorder: false,
          color: 'rgba(225,78,202,0.1)',
          zeroLineColor: 'transparent'
        },
        ticks: {
          padding: 20,
          fontColor: '#9a9a9a'
        }
      }]
    }
  }
});