<template>
  <div>
    <base-header class="pb-6 pb-8 pt-5 pt-md-8">
      <div class="row" v-if="selected_dam == null">
        <div class="col-xl-3 col-lg-6">
          <stats-card
            title="Total Dams"
            emoji="📈"
            type="gradient-info"
            :sub-title="damlength-1"
            class="mb-4 mb-xl-0"
          ></stats-card>
        </div>
        <div class="col-xl-3 col-lg-6">
          <stats-card
            title="Warn Dams"
            emoji="⚠️"
            type="gradient-warning"
            :sub-title="damwarn"
            class="mb-4 mb-xl-0"
          ></stats-card>
        </div>
        <div class="col-xl-3 col-lg-6">
          <stats-card
            title="Danger Dams"
            emoji="⛔"
            type="gradient-danger"
            :sub-title="damdanger"
            class="mb-4 mb-xl-0"
          ></stats-card>
        </div>
        <div class="col-xl-3 col-lg-6">
          <stats-card
            title="Normal Dam"
            emoji="✔️"
            type="gradient-success"
            :sub-title="damnormal"
            class="mb-4 mb-xl-0"
          ></stats-card>
        </div>
      </div>
      <div class="row" v-else>
        <div class="col-xl col-lg-6 p-1">
          <stats-card
            title="Dam Name 🌊"
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
            :sub-title="selected_dam.mwl_level ? selected_dam.mwl_level : '-'"
            class="mb-4 mb-xl-0 text-sm"
            subTitleClasses="h4 text-orange"
          ></stats-card>
        </div>
        <div class="col-xl col-lg-6 p-1" v-if="selected_dam.hfl_level">
          <stats-card
            title="HFL level (m)"
            type="gradient-warning"
            :sub-title="selected_dam.hfl_level ? selected_dam.hfl_level : '-'"
            class="mb-4 mb-xl-0"
            subTitleClasses="h4 text-danger"
          ></stats-card>
        </div>
        <div class="col-xl col-lg-6 p-1" v-if="selected_dam.warning_level">
          <stats-card
            title="Warning level (m)"
            type="gradient-danger"
            :sub-title="selected_dam.warning_level ? selected_dam.warning_level : '-'"
            class="mb-4 mb-xl-0"
            subTitleClasses="h4 text-yellow"
          ></stats-card>
        </div>
        <div class="col-xl col-lg-6 p-1" v-if="selected_dam.danger_level">
          <stats-card
            title="Danger level (m)"
            type="gradient-success"
            :sub-title="selected_dam.danger_level ? selected_dam.danger_level : '-'"
            class="mb-4 mb-xl-0"
            subTitleClasses="h4 text-orange"
          ></stats-card>
        </div>
      </div>
    </base-header>
    <div class="container-fluid mt--7">
      <div class="row mb-3">
        <div class="col-sm-7 mb-2 rounded" style="height:500px;">
          <div style="height:450px;">
          <base-alert type="secondary" classes="mb-0 border-0 rounded-0 rounded-top">
            <strong v-if="selected_dam == null">Map Summary 🌎</strong><br v-if="selected_dam == null"> 
            <small  v-if="selected_dam == null">(Hover over map to check any dam statistics)</small>
            <small  v-else><button
            class="btn btn-sm btn-primary"
            @click="setstatetoinitialstate"
          >
            Click to go back
          </button></small>
          </base-alert>
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
                v-if="dam.status=='Warning'"
                src="https://img.icons8.com/ios-filled/19/ffbe0b/filled-circle.png"
              />
              <img
                slot="marker"
                v-if="dam.status=='Normal'"
                src="https://img.icons8.com/ios-filled/19/3792cb/filled-circle.png"
              />
              <img
                slot="marker"
                v-if="dam.status=='Danger'"
                src="https://img.icons8.com/ios-filled/19/fb6340/filled-circle.png"
              />
              <MglPopup>
                <div>
                  {{ dam.name }}
                  <span :class="`text-${dam.status.toLowerCase()}`">({{dam.status}})</span>
                </div>
              </MglPopup>
            </MglMarker>
          </MglMap>
        </div>
        </div>
        <div class="col-sm-5 mb-2">
          <flood-summary v-if="selected_dam == null"></flood-summary>
          <dam-summary :dam="selected_dam" @setstatetoinitialstate="setstatetoinitialstate" v-else></dam-summary>
        </div>
      </div>
    </div>
    <chart-logic
      v-if="loaded"
      :damdata="dam_values"
      :forecastdata="forecast_values"
      :dam="selected_dam"
    />
  </div>
</template>
<script>
// // Charts
import FloodSummary from "../components/FloodSummary";
import DamSummary from "../components/DamSummary";
import ChartLogic from "../components/ChartLogic";
import { mapGetters, mapState } from "vuex";

import {
  MglMap,
  MglMarker,
  MglPopup,
  MglFullscreenControl,
  MglNavigationControl
} from "vue-mapbox";

export default {
  components: {
    MglMap,
    MglMarker,
    MglPopup,
    MglNavigationControl,
    MglFullscreenControl,
    FloodSummary,
    DamSummary,
    ChartLogic
  },
  data() {
    return {
      zoom: 3.5,
      center: [80, 23.07],
      accessToken:
        "pk.eyJ1IjoicHVzaHBhazEzMDAiLCJhIjoiY2ticmVyeWZnMnY3NDJzcXZ4eTgxeGlyYSJ9.15js0WpIdVUyDmoEmtfP3A", // your access token. Needed if you using Mapbox maps
      mapStyle: "mapbox://styles/pushpak1300/ckbs7pqao6z5u1imdve408b6v", // your map style
      selected_dam: null,
      dam_values: null,
      forecast_values: null,
      loaded: false
    };
  },
  computed: {
    ...mapState(["dams"]),
    ...mapGetters([
      "damwarn",
      "damdanger",
      "damnormal",
      "damwthlocation",
      "damlength"
    ])
  },
  created() {
    var vm = this;
    this.$http.get(""+process.env.VUE_APP_API_ENDPOINT+"dams").then(function(response) {
      vm.$store.commit("setDam", response.data);
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
    setstatetoinitialstate: function() {
      let center = [80, 23.07];
      var options = {
        center: center,
        zoom: 3.4,
        speed: 1.4,
        curve: 1
      };
      this.selected_dam = null;
      this.loaded = false;
      this.map.flyTo(options);
    },
    zoomtodam: function(dam) {
      let center = Array(dam.lon, dam.lat);
      var options = {
        center: center,
        zoom: 9.4,
        speed: 1.4,
        curve: 1
      };
      this.selected_dam = dam;
      this.map.flyTo(options);
      var vm = this;
      this.$http
        .get(""+process.env.VUE_APP_API_ENDPOINT+"dams/" + dam.id)
        .then(function(response) {
          vm.dam_values = response.data.values;
          vm.forecast_values = response.data.forecast;
          vm.loaded = true;
        });
    }
  }
};
</script>
