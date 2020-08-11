<template>
  <div>
    <base-header class="pb-5 pb-5 pt-6 pt-md-8"></base-header>
    <div class="container-fluid mt--7">
      <div class="row justify-content-center">
        <div class="col-lg-5 col-md-7">
          <div class="card bg-secondary shadow border-0">
            <div class="card-body px-lg-5 py-lg-5">
              <div class="text-center mb-4">
                <h2>Login Or Sign Up to Continue! </h2>
              </div>
              <form role="form">
                <base-input
                  class="input-group-alternative mb-3"
                  type="number"
                  placeholder="Mobile Number( 10 Digit number)"
                  :valid="valid.mobile"
                  :error="valid.mobile_error"
                  addon-left-icon="ni ni-mobile-button"
                  v-model="user.mobile"
                  :class="{otp_sent:'disabled'}"
                ></base-input>
                <div v-if="otp_sent===false">
                  <div class="text-center">
                    <base-button type="primary" @click="sendotp" class="my-4">Send OTP</base-button>
                  </div>
                </div>
                <div v-else>
                  <base-input
                    class="input-group-alternative"
                    placeholder="OTP"
                    type="text"
                    addon-left-icon="ni ni-lock-circle-open"
                    v-model="user.otp"
                  ></base-input>

                  <div class="text-center">
                    <base-button @click="login" type="primary" class="my-4">Go</base-button>
                  </div>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
export default {
  name: "login",
  data() {
    return {
      valid: {
        mobile: null,
        mobile_error: "",
        otp: true
      },
      otp_sent: false,
      user: {
        mobile: null,
        otp: ""
      }
    };
  },
  methods: {
    validate_mobile() {
      if (this.user.mobile.length != 10) {
        this.valid.mobile = false;
        this.valid.mobile_error = "Please Enter 10 digit mobile!";
      }
      if (this.otp_sent == true) {
        this.valid.otp = false;
      }
    },
    sendotp() {
      this.validate_mobile();
      var vm = this;
      this.$http
        .post(
          this.$api_url+"login/",
          this.$qs.stringify({ mobile: this.user.mobile })
        )
        .then(function(response) {
          if (response.data.message == "otp sent") {
            vm.otp_sent = true;
          }
        });
    },
    logout: function() {
      this.$store.dispatch('AUTH_LOGOUT').then(() => {
        delete this.$http.defaults.headers.common['Authorization'];
        this.$router.push("/login");
      });
    },
    login() {
      this.validate_mobile();
      var user = this.user.mobile;
      var otp = this.user.otp;
      var vm = this;
      this.$http
        .post(
          this.$api_url+"login/verify",
          this.$qs.stringify({ mobile: user, otp: otp })
        )
        .then(function(response) {
          vm.$store.commit("setLoading");
          console.log(response.data);
          var token = response.data.user.api_token;
          var user = response.data.user;
          localStorage.setItem("user-token", token);
          vm.$store.commit("setToken", token);
          vm.$store.commit("setUser", user);
          vm.$http.defaults.headers.common["Authorization"] = token;
          vm.$router.push("/notification");
        })
        .catch(err => {
          vm.$store.commit("setError");
          localStorage.removeItem("user-token");
          console.error(err);
        });
    }
  }
};
</script>
<style></style>
