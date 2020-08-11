<template>
  <div>
    <div>
      <base-header class="pb-6 pt-4 pt-md-8"></base-header>
      <div class="row justify-content-center mt--7">
        <div class="col-sm-8">
          <card
            header-classes="bg-transparent font-weight-bold h5 "
            classes="border border-primary"
            body-classes="p-1"
          >
            <div slot="header" class="row align-items-center p-2">
              <div class="col-sm-12 text-center">
                <h1 class="mb-0 pt-2 text-center pl-2">Enter Your Details!</h1>
                <small class="text-center">(We will send you notification on your email or number.)</small>
              </div>
            </div>
            <div class="container p-3 text-center">
              <div class="row px-3">
                <div class="col-sm-12">
                  <div class="form-group text-center px-lg-5" v-if="user!=null">
                    <label for="email">Email address(optional)</label>
                    <input
                      type="email"
                      class="form-control"
                      id="email"
                      v-model="value.email"
                      :placeholder="emailplaceholder"
                    />
                  </div>
                </div>
                <div class="col-sm-12">
                  <div class="form-group text-center px-lg-5" v-if="user!=null">
                    <label for="mobile">Mobile Number</label>
                    <input
                      type="number"
                      disabled
                      class="form-control"
                      id="mobile"
                      :placeholder="user.mobile"
                    />
                  </div>
                </div>
                <div class="col-sm-12" v-if="dams!=null">
                  <div class="form-group text-center px-lg-5">
                    <label for>Select dam for which you want to notified.</label>
                    <multiselect v-model="value.dam_id" :options="dams.dams"  label="name" track-by="name" :searchable="true" :allow-empty="false" placeholder="Select one">
                          <template slot="singleLabel" slot-scope="{ option }"><strong>{{ option.name }}</strong></template>
                    </multiselect>
                    <!-- <select class="custom-select" v-model="value.dam_id" v-if="dams!=null">
                      <option value disabled selected>Select Dam</option>
                      <option v-for="dam in dams.dams" :key="dam.id" :value="dam.id">{{dam.name}}</option>
                    </select> -->
                  </div>
                </div>
                <div class="col-sm-12">
                  <div class="form-group text-center px-lg-5">
                    <label for>Notification Type</label>
                    <div class="row">
                      <div class="col-sm-4">
                        <base-checkbox class="mb-2" v-model="checkbox.em">Email</base-checkbox>
                      </div>
                      <div class="col-sm-4">
                        <base-checkbox class="mb-2" v-model="checkbox.mo">SMS</base-checkbox>
                      </div>
                      <div class="col-sm-4">
                        <base-checkbox
                          class="mb-2"
                          v-model="checkbox.pu"
                        >Push Notification (app required)*</base-checkbox>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              <base-button
                type="primary"
                @click="subscribe"
                icon="ni ni-bell-55"
              >Subscribe For Alert!</base-button>
            </div>
          </card>
        </div>
        <div class="col-sm-10">
          <subscribe-list ref="list" :dams="dams"></subscribe-list>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import { mapState } from "vuex";
import SubscribeList from "../components/SubscribeList";
import Multiselect from 'vue-multiselect'
export default {
  components: {
    SubscribeList,
    Multiselect
  },
  data() {
    return {
      value: {
        email: null,
        dam_id: null
      },
      checkbox: {
        em: false,
        mo: true,
        pu: false
      }
    };
  },
  computed: {
    ...mapState(["dams", "user"]),
    emailplaceholder() {
      if (this.user.email == null) {
        return "email@email.com";
      } else {
        return String(this.user.email);
      }
    },
  },
  methods: {
    subscribe() {
      var vm = this;
      var config = {
        method: "post",
        url: "" + process.env.VUE_APP_API_ENDPOINT + "login/create/subscribe",
        data: this.$qs.stringify({
          email: this.value.email==null?undefined:this.value.email,
          dam_id: this.value.dam_id['id'],
          em: this.checkbox.em,
          mo: this.checkbox.mo,
          pu: this.checkbox.pu
        })
      };
      // console.log(config['data']);
      this.$http(config)
        .then(function(response) {
          vm.$refs.list.pushvalue(response.data.subscribe);
          // vm.subcription.push(response.data.subscribe);
          vm.value = {
            email: null,
            dam_id: null,
            em: false,
            mo: false,
            pu: false
          };
          vm.$swal({
            icon: "success",
            title: "Added Sucessfully"
          });
        })
        .catch(function(error) {
          console.log(error);
        });
    }
  },
  
};
</script>
<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>
<style></style>
