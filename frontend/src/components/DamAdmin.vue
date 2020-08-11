<template>
<div class="col-xl-12">
  <div class="col-xl-8 p-5" v-if="dams!=null">
    <div class="card">
      <div class="card-header border-0">
        <div class="row align-items-center">
          <div class="col">
            <h3 class="mb-0">Dam Status</h3>
          </div>
          <div class="col text-right">
            <a href="#!" class="btn btn-sm btn-primary">Send Notification</a>
          </div>
        </div>
      </div>
      <div class="table-responsive">
        <table class="table tablesorter">
          <thead class="thead-light">
            <tr>
              <th>Dam Code</th>
              <th>Dam Name</th>
              <th>Dam Status</th>
              <th>Edit</th>
            </tr>
          </thead>
          <tbody class>
            <tr v-for="dam in dams.dams" :key="dam.id">
              <th scope="row">{{dam.station_code}}</th>
              <td>{{dam.name}}</td>
              <td>{{dam.status}}</td>
              <td>
                <button class="btn btn-primary btn-sm" @click="openmodel(dam.id)">Edit</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    <modal :show.sync="open">
      <template slot="header">
        <h5 class="modal-title" id="exampleModalLabel">Change Status</h5>
      </template>
      <div>
        <div class="p-4">
          <label for="exampleFormControlSelect2">Change Dam Status to:</label>
          <select v-model="status" class="form-control form-control-lg">
            <option>Normal</option>
            <option>Warning</option>
            <option>Danger</option>
            <option>HFL levl</option>
          </select>
        </div>
      </div>
      <template slot="footer">
        <base-button type="secondary" @click="closemodal">Close</base-button>
        <base-button type="primary" @click="sumbit">Save changes</base-button>
      </template>
    </modal>
  </div>
 <div class="col-sm-5">

 </div>
 </div>
</template>

<script>
import { mapGetters } from "vuex";

export default {
  data() {
    return {
      open: false,
      status: null,
      selected: null
    };
  },
  computed: {
    ...mapGetters(["dams"])
  },
  methods: {
    openmodel(id) {
      this.selected = id;
      this.open = true;
    },
    closemodal() {
      this.open = false;
    },
    sumbit() {
      var config = {
        method: "post",
        url: this.$api_url + "staff/status/" + this.selected,
        data: this.$qs.stringify({
          status: this.status
        })
      };
      var vm = this;
      this.$http(config)
        .then(function(response) {
          var data = { dams: response.data.dam, id: vm.selected };
          vm.$store.commit("SetOneDam", data);
          vm.open = false;
        })
        .catch(function(error) {
          console.log(error);
        });
    }
  }
};
</script>

<style>
</style>