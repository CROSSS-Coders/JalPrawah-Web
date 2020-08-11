import Vue from "vue";
import Vuex from "vuex";
// import createLogger from 'vuex/dist/logger'

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    dams: null,
    token: localStorage.getItem('user-token') || '',
    status: '',
    user: null,
  },
  mutations: {
    setDam(state, data) {
      state.dams = data;
    },
    setLoading(state) {
      state.status = 'loading'
    },
    setToken(state, token) {
      state.status = 'success'
      state.token = token
    },
    setError(state) {
      state.status = 'error'
    },
    setUser(state, user) {
      state.user = user;
    },
    AUTH_LOGOUT(state) {
      state.token = null;
      state.user = null;
    },
    SetOneDam(state,data) {
      console.log(data.dams,data.id);
      state.dams.dams[data.id-1]=data.dams;
    },
  },
  getters: {
    isAuthenticated: state => !!state.token,
    authStatus: state => state.status,
    damwthlocation: state => {
      if (state.dams != null) {
        return state.dams.dams.filter(dam => dam.lat !== null);
      } else {
        return null;
      }
    },
    damlength: state => {
      if (state.dams != null) {
        return (state.dams.dams).length;
      } else {
        return null;
      }
    },
    damhfl: state => {
      if (state.dams != null) {
        return state.dams.dams.filter(dam => dam.status == "HFL").length;
      } else {
        return null;
      }
    },
    damwarn: state => {
      if (state.dams != null) {
        return state.dams.dams.filter(dam => dam.status == "Warning").length;
      } else {
        return null;
      }
    },
    damdanger: state => {
      if (state.dams != null) {
        return state.dams.dams.filter(dam => dam.status == "Danger").length;
      } else {
        return null;
      }
    },
    damnormal: state => {
      if (state.dams != null) {
        return state.dams.dams.filter(dam => dam.status == "Normal").length;
      } else {
        return null;
      }
    },
    dams:state=>{
        return state.dams;
      }

  },
  actions: {
    login_attempt(context, data) {
      data.vm.$http
        .post("http://127.0.0.1:5000/login/verify", data.vm.$qs.stringify({ mobile: data.mobile, otp: data.otp })
        )
        .then(function (response) {
          context.commit('setLoading');
          console.log(response.data);
          var token = response.data.message;
          localStorage.setItem('user-token', token);
          context.commit('setToken', token);
        })
        .catch(err => {
          context.commit('setError');
          localStorage.removeItem('user-token')
          console.error(err);
        });

    },
    AUTH_LOGOUT({ commit }){
      return new Promise((resolve) => {
        commit('AUTH_LOGOUT')
        localStorage.removeItem('user-token');
        resolve();
      })
    }
  },
  modules: {},
  // plugins: [createLogger()]
});
