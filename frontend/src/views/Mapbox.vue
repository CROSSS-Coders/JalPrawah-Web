<template>
  <div>
    <base-header type="gradient-success" class="pb-6 pb-8 pt-5 pt-md-8">
      <div class="row">
        <div class="col-xl-3 col-lg-6">
          <stats-card
            title="Total traffic"
            type="gradient-red"
            sub-title="350,897"
            icon="ni ni-active-40"
            class="mb-4 mb-xl-0"
          >
            <template slot="footer">
              <span class="text-success mr-2">
                <i class="fa fa-arrow-up"></i>
                3.48%
              </span>
              <span class="text-nowrap">Since last month</span>
            </template>
          </stats-card>
        </div>
        <div class="col-xl-3 col-lg-6">
          <stats-card
            title="Total traffic"
            type="gradient-orange"
            sub-title="2,356"
            icon="ni ni-chart-pie-35"
            class="mb-4 mb-xl-0"
          >
            <template slot="footer">
              <span class="text-success mr-2">
                <i class="fa fa-arrow-up"></i>
                12.18%
              </span>
              <span class="text-nowrap">Since last month</span>
            </template>
          </stats-card>
        </div>
        <div class="col-xl-3 col-lg-6">
          <stats-card
            title="Sales"
            type="gradient-green"
            sub-title="924"
            icon="ni ni-money-coins"
            class="mb-4 mb-xl-0"
          >
            <template slot="footer">
              <span class="text-danger mr-2">
                <i class="fa fa-arrow-down"></i>
                5.72%
              </span>
              <span class="text-nowrap">Since last month</span>
            </template>
          </stats-card>
        </div>
        <div class="col-xl-3 col-lg-6">
          <stats-card
            title="Performance"
            type="gradient-info"
            sub-title="49,65%"
            icon="ni ni-chart-bar-32"
            class="mb-4 mb-xl-0"
          >
            <template slot="footer">
              <span class="text-success mr-2">
                <i class="fa fa-arrow-up"></i>
                54.8%
              </span>
              <span class="text-nowrap">Since last month</span>
            </template>
          </stats-card>
        </div>
      </div>
    </base-header>

    <div class="container-fluid mt--7">
      <div class="row">
        <div class="col">
          <div class="card shadow border-0">
            <div id="map-canvas" style="height: 600px;">
              <MglMap
                :accessToken="accessToken"
                :zoom="zoom"
                :mapStyle.sync="mapStyle"
                :center="center"
                @load="onMapLoaded"
              >
                <MglNavigationControl position="top-left" />
                <MglFullscreenControl position="top-right" />
                <MglMarker
                  :coordinates="Array(dam.lon, dam.lat)"
                  v-for="dam in damwthlocation"
                  :key="dam.id"
                  color="red"
                  @click="zoomtodam(dam)"
                  @mouseenter="logname(dam)"
                  @mouseleave="logname(dam)"
                  :ref="'marker' + dam.id"
                >
                  <img
                    slot="marker"
                    src="https://img.icons8.com/fluent/20/000000/hydroelectric.png"
                  />
                  <!-- <i
                    slot="marker"
                    style="color:red;"
                    class="ni ni-air-baloon"
                  ></i> -->

                  <MglPopup>
                    <div>{{ dam.name }}</div>
                  </MglPopup>
                </MglMarker>
              </MglMap>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { MglMap, MglMarker, MglPopup, MglFullscreenControl ,MglNavigationControl,
  } from "vue-mapbox";

export default {
  components: {
    MglMap,
    MglMarker,
    MglPopup,
    MglNavigationControl,
    MglFullscreenControl

  },
  data() {
    return {
      dams: null,
      zoom:3.5,
      center:[80,23.07],
      accessToken:
        "pk.eyJ1IjoicHVzaHBhazEzMDAiLCJhIjoiY2ticmVyeWZnMnY3NDJzcXZ4eTgxeGlyYSJ9.15js0WpIdVUyDmoEmtfP3A", // your access token. Needed if you using Mapbox maps
      mapStyle: "mapbox://styles/pushpak1300/ckbs7pqao6z5u1imdve408b6v", // your map style
    };
  },
  computed: {
    damwthlocation: function() {
      if (this.dams != null) {
        return this.dams.dams.filter(dam => dam.lat !== null);
      } else {
        return null;
      }
    },
  },
  created() {
    var vm = this;
    this.$http.get(this.$api_url+"dams").then(function(response) {
      vm.dams = response.data;
    });
    this.map = null;
  },

  methods: {
    logname: function(dam) {
      this.$refs["marker" + dam.id][0].togglePopup();
    },
    onMapLoaded(event) {
      this.map = event.map;
      this.$store.map = event.map;
    },
    zoomtodam:function(dam){
      let center=Array(dam.lon,dam.lat);
      var options={
        center:center,
        zoom: 9.4,
        speed: 1.4,
        curve: 1,
      };      
      this.map.flyTo(options);
    }
  },
};
</script>
