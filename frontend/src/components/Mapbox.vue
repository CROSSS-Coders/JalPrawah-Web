<template>
  <MglMap
    :accessToken="accessToken"
    :hash="false"
    :zoom="3.4"
    :mapStyle.sync="mapStyle"
    :center="{ lon: 80, lat: 23.07 }"
  >
    <MglNavigationControl position="top-left" />
    <MglGeolocateControl position="top-right" />
    <MglMarker :coordinates="coordinates" color="red">
      <MglPopup>
        With supporting text below as a natural lead-in to additional content.
      </MglPopup>
    </MglMarker>
  </MglMap>
</template>

<script>
import Mapbox from "mapbox-gl";
import {
  MglMap,
  MglMarker,
  MglGeolocateControl,
  MglNavigationControl,
  MglPopup,
} from "vue-mapbox";

export default {
  components: {
    MglMap,
    MglMarker,
    MglGeolocateControl,
    MglNavigationControl,
    MglPopup,
  },
  data() {
    return {
      coordinates: [75.37, 19.48],
      accessToken:
        "pk.eyJ1IjoicHVzaHBhazEzMDAiLCJhIjoiY2ticmVyeWZnMnY3NDJzcXZ4eTgxeGlyYSJ9.15js0WpIdVUyDmoEmtfP3A", 
      mapStyle: "mapbox://styles/pushpak1300/ckbs7pqao6z5u1imdve408b6v", 
    };
  },

  created() {
    this.mapbox = Mapbox;
    console.log(this.mapbox);
    
  },
};
</script>

<style scoped>
button.mapboxgl-ctrl-active {
  background-color: #b7b7b7;
}
</style>
