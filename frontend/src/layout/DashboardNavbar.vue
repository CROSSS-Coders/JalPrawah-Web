<template>
  <base-nav class="navbar-top navbar-dark" id="navbar-main" :show-toggle-button="false" expand>
    <form class="navbar-search navbar-search-dark form-inline mr-3 d-none d-md-flex ml-lg-auto">
      <div class="form-group mb-0">
        <!-- <base-input
          placeholder="Search"
          class="input-group-alternative"
          alternative
          addon-right-icon="fas fa-search"
        ></base-input> -->
      </div>
    </form>
    <ul class="navbar-nav align-items-center d-none d-md-flex">
      <base-button v-if="isAuthenticated" type="secondary" @click="logout">
        <svg
          fill="none"
          style="height20px;width:20px;"
          stroke-linecap="round"
          stroke-linejoin="round"
          stroke-width="2"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            d="M11 16l-4-4m0 0l4-4m-4 4h14m-5 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h7a3 3 0 013 3v1"
          />
        </svg>Logout
      </base-button>
      <base-button
        v-else
        type="secondary"
        icon="ni ni-bell-55"
        @click="$router.push('/login')"
      >Subscribe For Alert!</base-button>

      <!-- <li class="nav-item dropdown">
        <base-dropdown class="nav-link pr-0">
          <div class="media align-items-center" slot="title">
            <span class="avatar avatar-sm rounded-circle">
              <img alt="Image placeholder" src="img/theme/team-4-800x800.jpg" />
            </span>
            <div class="media-body ml-2 d-none d-lg-block">
              <span class="mb-0 text-sm  font-weight-bold">Jessica Jones</span>
            </div>
          </div>

          <template>
            <div class=" dropdown-header noti-title">
              <h6 class="text-overflow m-0">Welcome!</h6>
            </div>
            <router-link to="/profile" class="dropdown-item">
              <i class="ni ni-single-02"></i>
              <span>My profile</span>
            </router-link>
            <router-link to="/profile" class="dropdown-item">
              <i class="ni ni-settings-gear-65"></i>
              <span>Settings</span>
            </router-link>
            <router-link to="/profile" class="dropdown-item">
              <i class="ni ni-calendar-grid-58"></i>
              <span>Activity</span>
            </router-link>
            <router-link to="/profile" class="dropdown-item">
              <i class="ni ni-support-16"></i>
              <span>Support</span>
            </router-link>
            <div class="dropdown-divider"></div>
            <router-link to="/profile" class="dropdown-item">
              <i class="ni ni-user-run"></i>
              <span>Logout</span>
            </router-link>
          </template>
        </base-dropdown>
      </li>-->
    </ul>
  </base-nav>
</template>
<script>
import { mapGetters } from "vuex";

export default {
  data() {
    return {
      activeNotifications: false,
      showMenu: false,
      searchQuery: ""
    };
  },
  computed: {
    // mix the getters into computed with object spread operator
    ...mapGetters(["isAuthenticated"])
  },
  methods: {
    toggleSidebar() {
      this.$sidebar.displaySidebar(!this.$sidebar.showSidebar);
    },
    hideSidebar() {
      this.$sidebar.displaySidebar(false);
    },
    toggleMenu() {
      this.showMenu = !this.showMenu;
    },
    logout: function() {
      this.$store.dispatch("AUTH_LOGOUT").then(() => {
        delete this.$http.defaults.headers.common["Authorization"];
        this.$router.push("/login");
      });
    }
  }
};
</script>
