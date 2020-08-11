<template>
  <div class="wrapper" :class="{ 'nav-open': $sidebar.showSidebar }">
    <side-bar :background-color="sidebarBackground" short-title="Argon" title="JalPravh">
      <template slot="links">
        <sidebar-item
          :link="{
            name: 'Dashboard',
            icon: 'ni ni-tv-2 text-primary',
            path: '/dashboard'
          }"
        />
        <sidebar-item
          :link="{
            name: 'Hardware Model',
            icon: 'ni ni-planet text-blue',
            path: '/iot'
          }"
        />
        <sidebar-item
          :link="{
            name: 'Notification',
            icon: 'ni ni-pin-3 text-orange',
            path: '/notification'
          }"
        />
        <sidebar-item
          v-if="user!=null && user.role!='user' "
          :link="{
            name: 'Admin',
            icon: 'ni ni-collection text-purple',
            path: '/staff'
          }"
        />
      </template>
    </side-bar>
    <div class="main-content" :data="sidebarBackground">
      <dashboard-navbar></dashboard-navbar>

      <div @click="toggleSidebar">
        <fade-transition :duration="200" origin="center top" mode="out-in">
          <router-view></router-view>
        </fade-transition>
        <content-footer v-if="!$route.meta.hideFooter"></content-footer>
      </div>
    </div>
  </div>
</template>
<script>
import DashboardNavbar from "./DashboardNavbar.vue";
import ContentFooter from "./ContentFooter.vue";
import { FadeTransition } from "vue2-transitions";
import { mapState } from 'vuex';

export default {
  components: {
    DashboardNavbar,
    ContentFooter,
    FadeTransition
  },
  computed: mapState(['user']),
  data() {
    return {
      sidebarBackground: "blue" //vue|blue|orange|green|red|primary
    };
  },
  methods: {
    toggleSidebar() {
      if (this.$sidebar.showSidebar) {
        this.$sidebar.displaySidebar(false);
      }
    }
  }
};
</script>
<style lang="scss"></style>
