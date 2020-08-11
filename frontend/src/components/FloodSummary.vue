<template>
  <div class="mt-4">
    <card
      header-classes="bg-transparent font-weight-bold h5 p-2 border-none"
      classes="border border-primary "
      body-classes="p-1 "
    >
      <div slot="header" class="row align-items-center">
        <div class="col-sm-12 text-center">
          <h6 class="text-uppercase ls-1 mb-1">FLOOD SITUATION SUMMARY 🌊</h6>
        </div>
      </div>
      <div>
        <table class="table text-center table-bordered border-blue border table-responsive">
          <thead class="text-center">
            <tr>
              <th scope="col">Flood Situations</th>
              <th scope="col">Numbers of Sites</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td class="text-wrap">
                <span class="font-weight-bold text-danger h4">Extreme Flood Situation</span>
                <br />(Site where the previous Highest Flood Level (HFL) is
                exceeded or equalled)
              </td>
              <td class="h1 text-danger">{{damhfl}}</td>
            </tr>
            <tr>
              <td class="text-wrap">
                <span class="font-weight-bold text-orange h4">Severe Flood Situation</span>
                <br />(Site where water level is touching or exceeding the Danger
                Level but below Highest Flood Level (HFL))
              </td>
              <td class="h1 text-orange">{{damdanger}}</td>
            </tr>
            <tr>
              <td class="text-wrap">
                <span class="font-weight-bold text-yellow h4">Above Normal Flood Situation:</span>
                <br />(Site where water level is touching or exceeding the Warning
                Level but below Danger Level)
              </td>
              <td class="h1 text-yellow">{{damwarn}}</td>
            </tr>
            <tr>
              <td class="text-wrap">
                <span class="font-weight-bold text-green h4">Total Sites Where Warning Issued</span>
              </td>
              <td class="h1 text-green">{{totalwarning}}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </card>
  </div>
</template>

<script>
import Card from "./Card.vue";
import { mapGetters } from "vuex";

export default {
  name: "flood-summary",
  components: {
    Card
  },
  computed: {
    totalwarning: function() {
      return this.damhfl + this.damwarn + this.damdanger;
    },
    ...mapGetters(["damwarn", "damdanger", "damnormal", "damhfl"])
  }
};
</script>

<style >
.table.no-cellpadding td {
  padding: 0px;
}
.card .table td,
.card .table th {
  padding-left: 0.4rem;
  padding-right: 0.4rem;
}
.card-header {
  border-bottom: 0px;
}
</style>
