import Vue from "vue";
import VueRouter from "vue-router";
import DashboardLayout from "@/layout/DashboardLayout";
import AuthLayout from "@/layout/AuthLayout";
import store from '../store/index' 

Vue.use(VueRouter);


const ifNotAuthenticated = (to, from, next) => {
  if (!store.getters.isAuthenticated) {
    next()
    return
  }
  next('/notification')
}

const ifAuthenticated = (to, from, next) => {
  if (store.getters.isAuthenticated) {
    next()
    return
  }
  next('/login')
}


const routes = [
  
  {
    path: "/",
    redirect: "dashboard",
    component: DashboardLayout,
    children: [
      {
        path: "/dashboard",
        name: "dashboard",
        component: () => import("@/views/Dashboard.vue")
      },
      {
        path: "/iot",
        name: "iot",
        component: () => import("@/views/Iot.vue")
      },
      {
        path: "/profile",
        name: "profile",
        component: () => import("@/views/UserProfile.vue")
      },
      {
        path: "/notification",
        name: "notification",
        beforeEnter: ifAuthenticated,
        component: () => import("@/views/Notification.vue")
      },
      {
        path: "/login",
        name: "login",
        component: () => import("@/views/Login.vue"),
        beforeEnter: ifNotAuthenticated
      },
      {
        path: "/staff",
        name: "staff",
        component: () => import("@/views/Staff.vue")
      }
    ]
  },
  {
    path: "/",
    redirect: "login",
    component: AuthLayout,
    children: [
      {
        path: "/logins",
        name: "logins",
        component: () => import("@/views/Login.vue")
      },
      {
        path: "/register",
        name: "register",
        component: () => import("@/views/Register.vue")
      }
    ]
  },

];

const router = new VueRouter({
  base: process.env.BASE_URL,
  routes
});

export default router;
