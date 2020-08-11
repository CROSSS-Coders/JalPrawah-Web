<template>
  <div>
    <div v-if="loading" class="loading">Loading...</div>
    <div v-else>
      <base-header class="pb-6 pb-8 pt-5 pt-md-8">
        <div class="row" v-if="selected_dam!=null">
          <div class="col-xl col-lg-6 p-1">
            <stats-card
              title="Dam Name"
              type="gradient-info"
              :sub-title="selected_dam.name"
              class="mb-4 mb-xl-0 text-sm"
              subTitleClasses="h4"
            ></stats-card>
          </div>
          <div class="col-xl col-lg-6 p-1" v-if="selected_dam.frl_level">
            <stats-card
              title="Frl Level"
              type="gradient-info"
              :sub-title="selected_dam.frl_level ? selected_dam.frl_level : '-'"
              class="mb-4 mb-xl-0 text-sm"
              subTitleClasses="h4 text-blue"
            ></stats-card>
          </div>
          <div class="col-xl col-lg-6 p-1" v-if="selected_dam.mwl_level">
            <stats-card
              title="MWL level"
              type="gradient-info"
              :sub-title="selected_dam.mwl_level ? selected_dam.mwl_level  : '-'"
              class="mb-4 mb-xl-0 text-sm"
              subTitleClasses="h4 text-orange"
            ></stats-card>
          </div>
          <div class="col-xl col-lg-6 p-1" v-if="selected_dam.hfl_level">
            <stats-card
              title="HFL level (cm)"
              type="gradient-warning"
              :sub-title="selected_dam.hfl_level ? selected_dam.hfl_level : '-'"
              class="mb-4 mb-xl-0"
              subTitleClasses="h4 text-danger"
            ></stats-card>
          </div>
          <div class="col-xl col-lg-6 p-1" v-if="selected_dam.warning_level">
            <stats-card
              title="Warning level (cm)"
              type="gradient-danger"
              :sub-title="selected_dam.warning_level ? selected_dam.warning_level : '-'"
              class="mb-4 mb-xl-0"
              subTitleClasses="h4 text-yellow"
            ></stats-card>
          </div>
          <div class="col-xl col-lg-6 p-1" v-if="selected_dam.danger_level">
            <stats-card
              title="Danger level (cm)"
              type="gradient-success"
              :sub-title="selected_dam.danger_level ? selected_dam.danger_level : '-'"
              class="mb-4 mb-xl-0"
              subTitleClasses="h4 text-orange"
            ></stats-card>
          </div>
        </div>
      </base-header>
      <div class="container-fluid mt--7">
        <div class="row">
          <div class="col-sm-6 mb-5 mb-xl-0" style="height:500px;">
            <card header-classes="bg-transparent">
              <div slot="header" class="row align-items-center">
                <div class="col-sm-12">
                  <h6 class="text-uppercase ls-1 mb-1 pt-3 pl-4 text-center">Real Time Water Level</h6>
                </div>
              </div>
              <apexchart :height="360" ref="chart" type="line" :options="options" :series="series"></apexchart>
            </card>
          </div>
          <div class="col-sm-6 mb-2">
            <card header-classes="bg-transparent font-weight-bold h5 " body-classes="p-1">
              <div slot="header" class="row align-items-center p-2">
                <div class="col-sm-12">
                  <h5 class="h3 mb-0 pt-2 text-center pl-2">Real time summary</h5>
                </div>
              </div>
              <div>
                <ul class="list-group list-group-flush list my-1">
                  <li class="list-group-item px-0">
                    <div class="row align-items-center">
                      <div class="col-auto"></div>
                      <div class="col">
                        <h5 class="mb-0">Current Flood Situation</h5>
                      </div>
                      <div class="col">
                        <h3 class="mb-0">Normal</h3>
                      </div>
                    </div>
                  </li>
                  <li class="list-group-item px-0">
                    <div class="row align-items-center">
                      <div class="col-auto"></div>
                      <div class="col">
                        <h5 class="mb-0">Humidity</h5>
                        <small v-text="new Date().toDateString()"></small>
                      </div>
                      <div class="col">
                        <h3 class="mb-0">{{latest_dam.humidity}} %</h3>
                      </div>
                    </div>
                  </li>
                  <li class="list-group-item px-0">
                    <div class="row align-items-center">
                      <div class="col-auto"></div>
                      <div class="col">
                        <h5 class="mb-0">Pressure on Dam:</h5>
                      </div>
                      <div class="col">
                        <h4 class="mb-0">{{latest_dam.pressure}} Pascal</h4>
                      </div>
                    </div>
                  </li>
                  <li class="list-group-item px-0">
                    <div class="row align-items-center">
                      <div class="col-auto"></div>
                      <div class="col">
                        <h5 class="mb-0">Door Open:</h5>
                      </div>
                      <div class="col">
                        <h4 class="mb-0">{{door_open}}</h4>
                      </div>
                    </div>
                  </li>
                  <li class="list-group-item px-0">
                    <div class="row align-items-center">
                      <div class="col-auto"></div>
                      <div class="col">
                        <h5 class="mb-0">Water Level:</h5>
                      </div>
                      <div class="col">
                        <h4 class="mb-0">{{latest_dam.water_level}} cm</h4>
                      </div>
                    </div>
                  </li>
                  <li class="list-group-item px-0">
                    <div class="row align-items-center">
                      <div class="col-auto"></div>
                      <div class="col">
                        <h5 class="mb-0">Flood Prediction:</h5>
                      </div>
                      <div class="col">
                        <h4 class="mb-0">{{latest_dam.forecast_value}}</h4>
                      </div>
                    </div>
                  </li>
                  <li class="list-group-item px-0">
                    <div class="row align-items-center">
                      <div class="col-auto"></div>
                      <div class="col">
                        <h5 class="mb-0">Tempreture:</h5>
                      </div>
                      <div class="col">
                        <h4 class="mb-0">{{latest_dam.temperature}} °C</h4>
                      </div>
                    </div>
                  </li>
                </ul>
              </div>
            </card>
          </div>
          <!-- <div class="col-sm-12">
            <card header-classes="bg-transparent" classes="border border-primary">
              <div slot="header" class="row align-items-center">
                <div class="col-sm-12 text-center">
                  <h4 class="text-uppercase ls-1 mb-1 pt-3 pl-4">
                    Water Level
                    <span class="h2">🌡️</span>
                    <small>(Historic Data)</small>
                    & Forecast level
                    <span class="h2">☀️</span>
                    <small>(Next 3 days)</small>
                  </h4>
                </div>
              </div>
              <apexchart :height="210" type="area" :options="optionss" :series="seriess"></apexchart>
            </card>
          </div>-->
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import Pusher from "pusher-js";
import VueApexCharts from "vue-apexcharts";

export default {
  components: {
    apexchart: VueApexCharts
  },
  data() {
    return {
      loading: false,
      shown_warning: false,
      shown_danger: false,
      values: null,
      options: {
        chart: {
          type: "line",
          animations: {
            enabled: true,
            easing: "linear",
            dynamicAnimation: {
              speed: 1000
            }
          }
        },
        dataLabels: {
          enabled: false
        },
        annotations: {
          yaxis: [
            {
              y: 17,
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
            },
            {
              y: 20.5,
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
                text: "Danger Level"
              },
              text: "Danger level"
            },
            {
              y: 25,
              borderColor: "#e63946",
              label: {
                position: "left",
                offsetX: 220,
                borderColor: "#e63946",
                style: {
                  color: "#fff",
                  background: "#e63946"
                },
                text: "FRL level"
              }
            }
          ]
        },
        legend: {
          show: false
        },
        yaxis: {
          title: {
            text: "Level"
          },
          max: 25,
          min: 0
        }
      },
      series: [
        {
          name: "Water level",
          data: []
        }
      ],
      
      seriess: [
        {
          name: "Water level",
          data: []
        }
      ]
    };
  },
  computed: {
    selected_dam: function() {
      if (this.$store.state.dams != null) {
        return this.$store.state.dams.dams[32];
      } else {
        return null;
      }
    },
    latest_dam: function() {
      if (this.values != null) {
        return this.values.slice(-1).pop();
      } else {
        return null;
      }
    },
    door_open: function() {
      if (this.values != null) {
        if (this.latest_dam.door_open_code == 2) {
          return "2 Doors Open";
        }
        if (this.latest_dam.door_open_code == 1) {
          return "1 Doors Open";
        } else {
          return "Doors are closed";
        }
      } else {
        return null;
      }
    }
  },
  created() {
    this.loading = true;
    this.fetchdata();
  },
  methods: {
    fetchdata() {
      var vm = this;
      if (this.$store.state.dams == null) {
        this.$http
          .get("" + process.env.VUE_APP_API_ENDPOINT + "/dams")
          .then(function(response) {
            vm.$store.commit("setDam", response.data);
          });
      }
      this.$http
        .get("" + process.env.VUE_APP_API_ENDPOINT + "/iot")
        .then(function(response) {
          vm.values = response.data.values;
          vm.series[0].data = vm.values
            .map(function(value) {
              return { y: value.water_level, x: value.date };
            })
            .slice(Math.max(vm.values.length - 5, 1));
          // vm.seriess[0].data = vm.values.map(function(value) {
          //   return { y: value.water_level, x: value.date };
          // });
          vm.subscribe();
          vm.loading = false;
        });
    },
    subscribe() {
      // Pusher.logToConsole = true;
      let pusher = new Pusher("d121a0e4fc8e52e1b0ab", { cluster: "ap2" });
      let subscribe = pusher.subscribe("iot");
      var vm = this;
      subscribe.bind("updated", function(data) {
        vm.updatechart(data);
        console.log(data);
        if (vm.shown_danger==false && data.message.water_level>20.5) {
          vm.$swal({
            icon: "warning",
            timer: 6000,
            title: "Water Reached Danger Level!"
          });
          vm.shown_danger=true;
        }
      });
    },
    resetData() {},
    updatechart(newdata) {
      let vm = this;
      vm.values.push(newdata.message);
      let data = vm.series[0].data;
      data.shift();
      data.push({ x: newdata.message.date, y: newdata.message.water_level });
      vm.$refs.chart.updateSeries(
        [
          {
            name: "Water level",
            data: data
          }
        ],
        true
      );

      // window.setInterval(function() {
      //   vm.$refs.chartss.updateSeries(
      //     [
      //       {
      //         name: "Water level",
      //         data: data
      //       },
      //       true
      //     ],
      //     false,
      //     true
      //   );
      // }, 600000);
    }
  }
};
</script>
<style></style>
