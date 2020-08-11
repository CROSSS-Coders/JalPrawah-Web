<template>
  <div class="container-fluid mt-5">
    <div class="row">
      <div class="col-sm-12">
        <card header-classes="bg-transparent" classes="border border-primary">
          <div slot="header" class="row align-items-center">
            <div class="col-sm-12 text-center">
              <h4 class="text-uppercase ls-1 mb-1 pt-3 pl-4">
                Water Level
                <span class="h2">🌡️</span><small>(Historic Data)</small>
               & Forecast level
                <span class="h2">☀️</span> <small>(Next 3 days)</small>
              </h4>
            </div>
          </div>
          <apexchart :height="210" type="area" :options="options" :series="series"></apexchart>
        </card>
      </div>
      <!-- <div class="col-sm-6">
        <card header-classes="bg-transparent" classes="border border-primary">
          <div slot="header" class="row align-items-center">
            <div class="col-sm-12 text-center">
              <h4 class="text-uppercase ls-1 mb-1 pt-3 pl-4">
                Forecasted Model
                <span class="h2">☀️</span> <small>(Next 3 days)</small>
              </h4>
            </div>
          </div>
          <apexchart :height="210" type="area" :options="options" :series="series_forecast"></apexchart>
        </card>
      </div> -->
    </div>
  </div>
</template>

<script>
import VueApexCharts from "vue-apexcharts";

export default {
  name: "chart-logic",
  components: {
    apexchart: VueApexCharts
  },
  props: {
    damdata: {
      type: [String, Object, Array],
      description: "Dam Data Values"
    },
    forecastdata: {
      type: [String, Object, Array],
      description: "Forecast Data Values"
    },
    dam: {
      type: [String, Object, Array]
    }
  },
  data() {
    return {
      options: {
        chart: {
          type: "area"
        },
        colors: ["#5e72e4","#123456"],
        stroke: {
          width: [4,5],
          curve: "straight",
          dashArray: [0, 5]
        },
        fill: {
          type: "gradient",
          gradient: {
            shadeIntensity: 1,
            inverseColors: false,
            opacityFrom: 0.5,
            opacityTo: 0,
            stops: [0, 90, 100]
          }
        },
        dataLabels: {
          enabled: false
        },
        xaxis: {
          type: "datetime"
        },
        yaxis: {
          max: null,
          forceNiceScale: true
        },
        annotations: {
          position: "front",
          yaxis: []
        }
      },
      series: [
        {
          name: "water level",
          data: []
        },
        {
          name: "Forecst level",
          data: []
        }
      ],
      series_forecast: [
        {
          name: "water level",
          data: []
        }
      ],
      maxarray: []
    };
  },
  created() {
    // this.options.xaxis.categories = this.damdata.map(
    //   value => value.datatime
    // );
    // this.series_forecast[0].data = this.forecastdata.map(value => value.water_level);
    // this.series[0].data = this.damdata.map(value => value.value);
    this.series[1].data = this.forecastdata.map(function(value) {
      return { y: value.water_level, x: value.datatime };
    });
    this.series[0].data = this.damdata.map(function(value) {
      return { y: value.value, x: value.date };
    });
    if (this.dam.warning_level != null) {
      var config = {
        y: this.dam.warning_level,
        borderColor: "#ffba08",
        label: {
          borderWidth: 1,
          position: "left",
          borderColor: "#ffba08",
          offsetX: 100,
          style: {
            color: "#fff",
            background: "#ffba08",
            fontSize: 12
          },
          text: "Warning Level"
        }
      };

      this.maxarray.push(this.dam.warning_level);
      this.options.annotations.yaxis.push(config);
    }
    if (this.dam.danger_level != null) {
      var config2 = {
        y: this.dam.danger_level,
        borderColor: "#e63946",
        label: {
          position: "left",
          offsetX: 220,
          borderColor: "#e63946",
          style: {
            color: "#fff",
            background: "#e63946",
            fontSize: 12
          },
          text: "Danger level"
        }
      };
      this.maxarray.push(this.dam.danger_level);
      this.options.annotations.yaxis.push(config2);
    }
    if (this.dam.hfl_level != null) {
      var config4 = {
        y: this.dam.hfl_level,
        borderColor: "#ffba08",
        label: {
          offsetX: -100,
          borderColor: "#ffba08",
          style: {
            color: "#fff",
            background: "#ffb468"
          },
          text: "HFL Level"
        }
      };
      this.maxarray.push(this.dam.hfl_level);
      this.options.annotations.yaxis.push(config4);
    }
    if (this.dam.frl_level != null) {
      var config5 = {
        y: this.dam.frl_level,
        borderColor: "#ffba08",
        label: {
          offsetX: -200,
          borderColor: "#ffba08",
          style: {
            color: "#fff",
            background: "#ffba08"
          },
          text: "Frl Level"
        }
      };
      this.maxarray.push(this.dam.frl_level);
      this.options.annotations.yaxis.push(config5);
    }
    if (this.dam.mwl_level != null) {
      var config6 = {
        y: this.dam.mwl_level,
        borderColor: "#ffba08",
        label: {
          borderColor: "#ffba08",
          style: {
            color: "#fff",
            background: "#ffba08"
          },
          text: "MWL Level"
        }
      };
      this.maxarray.push(this.dam.mwl_level);
      this.options.annotations.yaxis.push(config6);
    }
    var max = Math.max(...this.damdata.map(value => value.value));
    this.maxarray.push(max);
    var maxs = Math.max(...this.maxarray);
    this.options.yaxis.max = maxs;
  }
};
</script>

<style>
</style>