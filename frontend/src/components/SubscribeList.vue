<template>
  <!-- <div class="row p-2">
  <div class="col-sm-6 p-2" v-for="item in subcription" :key="item.id">-->
  <!-- <card
        header-classes="bg-transparent font-weight-bold h5 "
        classes="border border-primary "
        body-classes="p-1"
  >-->
  <!-- <div slot="header" class="row align-items-center p-2">
          <div class="col-sm-12 text-center" v-if="dams!=null">
            <h4 class="mb-0 pt-1 text-center pl-2" v-text="getdamname(item.id)"></h4>
            <small class="text-center">River : ({{getrivername(item.id)}})</small>
          </div>
  </div>-->
  <div class="row p-2" v-if="dams!=null">
    <div class="col-sm-12 p-2" v-if="subcription.len!=0">
      <div class="card shadow">
        <div class="card-header border-0">
          <div class="row align-items-center">
            <div class="col">
              <h3 class="mb-0">Subscribed Dams</h3>
            </div>
            <div class="col text-right">
              <button type="button" class="btn btn-primary btn-sm">See all</button>
            </div>
          </div>
        </div>
        <div class="table-responsive">
          <table class="table tablesorter table align-items-center table-flush">
            <thead class="thead-light">
              <tr>
                <th>Dam</th>
                <th>River</th>
                <th>Eamil</th>
                <th>SMS</th>
                <th>App</th>
                <th>Edit</th>
                <th>Delete</th>
              </tr>
            </thead>
            <tbody class="list">
              <tr v-for="item in subcription" :key="item.id">
                <th scope="row">
                  <div class="media align-items-center">
                    <a href="#" class="avatar rounded-circle mr-3">
                      <img
                        src="https://img.icons8.com/doodle/48/000000/hydroelectric.png"
                        class="image-placeholder"
                      />
                    </a>
                    <div class="media-body">
                      <span class="name mb-0 text-sm">{{getdamname(item.dam_id)}}</span>
                    </div>
                  </div>
                </th>
                <td class="budget">{{getrivername(item.dam_id)}}</td>
                <td>
                  <span class="status">
                    <label class="custom-toggle">
                      <input type="checkbox" v-model="item.email" v-bind="$attrs" v-on="$listeners" />
                      <span class="custom-toggle-slider rounded-circle"></span>
                    </label>
                  </span>
                </td>
                <td>
                  <span class="status">
                    <label class="custom-toggle">
                      <input
                        type="checkbox"
                        v-model="item.mobile"
                        v-bind="$attrs"
                        v-on="$listeners"
                      />
                      <span class="custom-toggle-slider rounded-circle"></span>
                    </label>
                  </span>
                </td>
                <td>
                  <div class="d-flex align-items-center">
                    <label class="custom-toggle">
                      <input type="checkbox" v-model="item.push" v-bind="$attrs" v-on="$listeners" />
                      <span class="custom-toggle-slider rounded-circle"></span>
                    </label>
                  </div>
                </td>
                <td>
                  <div @click="update(item.id)" class="d-flex align-items-center">
                    <svg
                      class="text-primary"
                      style="height:18px;width:18px;"
                      fill="none"
                      viewBox="0 0 24 24"
                      stroke="currentColor"
                    >
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2"
                        d="M12 6V4m0 2a2 2 0 100 4m0-4a2 2 0 110 4m-6 8a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4m6 6v10m6-2a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4"
                      />
                    </svg>
                  </div>
                </td>
                <td>
                  <div @click="deleteitem(item.id)" class="d-flex align-items-center">
                    <svg
                      class="text-danger"
                      style="height:18px;width:18px;"
                      fill="none"
                      viewBox="0 0 24 24"
                      stroke="currentColor"
                    >
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2"
                        d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
                      />
                    </svg>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
  <!-- </card> -->
  <!-- </div>
  </div>-->
</template>

<script>
export default {
  props: ["dams"],
  data() {
    return {
      subcription: []
    };
  },
  mounted() {
    var vm = this;
    var config = {
      method: "get",
      url: "" + process.env.VUE_APP_API_ENDPOINT + "login/subscibe"
    };
    this.$http(config)
      .then(function(response) {
        vm.subcription = response.data.subscribe;
      })
      .catch(function(error) {
        console.log(error);
      });
  },
  methods: {
    getdamname(id) {
      var dam = this.dams.dams.find(sub => sub.id === id);;
      return dam.name;
    },
    getrivername(id) {
      var dam = this.dams.dams.find(sub => sub.id === id);
      return dam.river;
    },
    pushvalue(item) {
      this.subcription.push(item);
    },
    update(id) {
      var vm = this;
      var subscibe = this.subcription.find(sub => sub.id === id);
      var config = {
        method: "put",
        url: "" + process.env.VUE_APP_API_ENDPOINT + "login/subscibe/" + id,
        data: this.$qs.stringify({
          dam_id: subscibe.dam_id,
          em: subscibe.email,
          mo: subscibe.mobile,
          pu: subscibe.push
        })
      };
      this.$http(config)
        .then(function(response) {
          vm.subcription[response.data.subscribe.id] = response.data.subscribe;
          vm.$swal({
            icon: "success",
            title: "Updated Sucessfully"
          });
        })
        .catch(function(error) {
          console.log(error);
        });
    },
    deleteitem(id) {
      var vm = this;
      var config = {
        method: "delete",
        url:
          "" +
          process.env.VUE_APP_API_ENDPOINT +
          "login/subscibe/" +
          id +
          "/delete"
      };
      this.$http(config)
        .then(function(response) {
          vm.subcription = response.data.subscribe;
          vm.$swal({
            icon: "warning",
            title: "Deleted Sucessfully"
          });
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