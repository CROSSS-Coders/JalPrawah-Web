<template>
  <div class="col-xl-12 p-5" v-if="users!=null">
    <div class="card">
      <div class="card-header border-0">
        <div class="row align-items-center">
          <div class="col">
            <h3 class="mb-0">User Module</h3>
          </div>
          <div class="col text-right">
            <a href="#!" class="btn btn-sm btn-primary">ADD NEW STAFF</a>
          </div>
        </div>
      </div>
      <div class="table-responsive">
        <table class="table tablesorter">
          <thead class="thead-light">
            <tr>
              <th>User Id</th>
              <th>Email</th>
              <th>Mobile Number</th>
              <th>Role</th>
            </tr>
          </thead>
          <tbody class>
            <tr v-for="user in users" :key="user.id">
              <th scope="row">{{user.id}}</th>
              <td>{{user.email}}</td>
              <td>{{user.mobile}}</td>
              <td>{{user.role.toUpperCase()}}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
export default {
    data() {
    return {
      users: null
    };
  },
  mounted() {
    var config = {
      method: "get",
      url: this.$api_url + "staff/user"
    };
    var vm = this;
    this.$http(config).then(function(response) {
      vm.users = response.data.user;
    });
  }
};
</script>

<style>
</style>