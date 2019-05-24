<template>
  <div id="app">
    <Header />
    <div class="page-container">
       <div v-if="loading">loading...</div>
      <router-view :key="$route.fullPath" />
    </div>
    <Toast />
  </div>
</template>

<script>
import axios from 'axios';
import { mapState, mapActions, mapMutations } from 'vuex';
import store from './vuex';
import Header from '@/components/Header';
import Toast from '@/components/Toast';
import Settings from './vuex/modules/Settings';
import { API_URL } from '@/constants/';

export default {
  name: 'App',
  data() {
    return {
      loading: true,
    };
  },
  components: {
    Header,
    Toast,
  },
  computed: {
    ...mapState({
      signedIn: state => state.auth.signedIn,
      profile: state => state.auth.profile,
    }),
  },
  created() {
    this.loading = false;
  },
  mounted() {
    // Small duct-tape, fix after mvp
    const isSignedIn = localStorage.getItem('profile') ? true : false;
    this.$store.state.auth.signedIn = isSignedIn;
    
    if (isSignedIn) {
      const profile = JSON.parse(localStorage.getItem('profile'));
      const data = {
        token: profile.auth.profile.id_token,
      };
      axios.get(`${API_URL}/settings/?id_token=${profile.auth.profile.id_token}`)
        .then((response) => {
          const settings = response.data.result[0];
          this.colorChange(settings.color);
        })
        .catch((error) => {
          console.log({ error });
        });
    }
  },
  methods: {
    ...mapMutations('settings', [
      'colorChange',
      'nicknameChange',
    ])
  },
};
</script>

<style>
@import './App.css';
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
}
body {
  background-color: #f0f3f5 !important;
}

.page-container {
  margin-top: 44pt !important;
  margin: auto;
  max-width: 964pt;
  padding: 3pt 2vw;
  height: calc(100vh - 44pt);
}
</style>
