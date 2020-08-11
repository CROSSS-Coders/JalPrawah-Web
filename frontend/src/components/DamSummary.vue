<template>
  <div>
    <card
      header-classes="bg-transparent font-weight-bold h5 "
      body-classes="p-1"
      classes="border border-primary"
    >
      <div slot="header" class="row align-items-center p-2">
        <div class="col-8">
          <h5 class="h3 mb-0">Dam Summary 🌊</h5>
        </div>
        <div class="col-4 text-right">
          <button class="btn btn-sm btn-primary" @click="setstatetoinitialstate">Back</button>
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
                <h3 class="mb-0" :class="`text-${dam.status.toLowerCase()}`">{{dam.status}}</h3>
              </div>
            </div>
          </li>
          <!-- <li class="list-group-item px-0">
            <div class="row align-items-center">
              <div class="col-auto"></div>
              <div class="col">
                <h5 class="mb-0">Current Rainfall:</h5>
                <small v-text="new Date().toDateString()"></small>
              </div>
              <div class="col">
                <h3 class="mb-0">{{rain==undefined ? 0 :rain }} mm</h3>
              </div>
            </div>
          </li> -->
          <li class="list-group-item px-0">
            <div class="row align-items-center">
              <div class="col-auto"></div>
              <div class="col">
                <h5 class="mb-0">River:</h5>
              </div>
              <div class="col">
                <h4 class="mb-0">{{dam.river}}</h4>
              </div>
            </div>
          </li>
          <li class="list-group-item px-0">
            <div class="row align-items-center">
              <div class="col-auto"></div>
              <div class="col">
                <h5 class="mb-0">District:</h5>
              </div>
              <div class="col">
                <h4 class="mb-0">{{dam.district}}</h4>
              </div>
            </div>
          </li>
          <li class="list-group-item px-0">
            <div class="row align-items-center">
              <div class="col-auto"></div>
              <div class="col">
                <h5 class="mb-0">Divisional Office:</h5>
              </div>
              <div class="col">
                <h4 class="mb-0">{{dam.office}}</h4>
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
                <h4 class="mb-0" :class="`text-${dam.status.toLowerCase()}`">{{dam.status}}</h4>
              </div>
            </div>
          </li>
        </ul>
      </div>
    </card>
  </div>
</template>

<script>
import Card from "./Card.vue";

export default {
  name: "dam-summary",
  props: {
    dam: {
      type: Object,
      description: "Dam Object"
    }
  },
  components: {
    Card
  },
  data() {
    return {
      rain: null
    };
  },
  mounted() {
    // var vm = this;
    // try {
    //   this.$http
    //     .get(
    //       "https://cors-anywhere.herokuapp.com/https://api.openweathermap.org/data/2.5/onecall?lat=" +
    //         vm.dam.lat +
    //         "&lon=" +
    //         vm.dam.lon +
    //         "&exclude=hourly,minutely,daily&appid=e2af5641a8245041b6a6741137f091d4"
    //     )
    //     .then(function(response) {
    //       console.log(response.data.current.rain);
    //       vm.rain = response.data.current.rain["1h"];
    //     });
    // } catch (error) {
    //   vm.rain = 0;
    // }
  },
  methods: {
    setstatetoinitialstate: function() {
      this.$emit("setstatetoinitialstate");
    }
  }
};
</script>

<style></style>
