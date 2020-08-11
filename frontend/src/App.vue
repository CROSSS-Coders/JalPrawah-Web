<template>
  <div id="app">
    <notifications></notifications>
    <router-view/>
  </div>
</template>

<script>
export default {
mounted() {
    var vm = this;
    if (this.$store.state.dams == null) {
      this.$http
        .get("" + process.env.VUE_APP_API_ENDPOINT + "dams")
        .then(function(response) {
          vm.$store.commit("setDam", response.data);
        });
    }
    if (this.$store.state.user == null && this.$store.getters.isAuthenticated==true) {
      this.$http
        .post("" + process.env.VUE_APP_API_ENDPOINT + "login/user")
        .then(function(response) {
          var token = response.data.user.api_token;
          var user = response.data.user;
          vm.$store.commit("setUser", user);
          vm.$http.defaults.headers.common["Authorization"] = token;
        });
    }
  }
}
</script>

