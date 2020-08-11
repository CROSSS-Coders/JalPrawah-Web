<template>
  <footer class="footer px-4">
    <div class="row align-items-center justify-content-lg-between">
      <div class="col-lg-6">
        <div class="copyright text-center text-lg-left text-muted">
          © {{ year }}
          <a
            href="#"
            class="font-weight-bold ml-1"
            target="_blank"
          >CROSSS_Coders</a>
        </div>
      </div>
      <div class="col-lg-6">
        <ul class="nav nav-footer justify-content-center justify-content-lg-end">
          <router-link to="/iot" class="nav-item">
              <span class='nav-link'>IOT</span>
            </router-link>
          <router-link to="/login" class="nav-item">
              <span class='nav-link'>Staff Login</span>
            </router-link>
        </ul>
      </div>
    </div>
  </footer>
</template>
<script>
export default {
  data() {
    return {
      year: new Date().getFullYear()
    };
  }
};
</script>
<style></style>
