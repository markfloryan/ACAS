<template>
  <!-- Signout.vue
    This is a "fake" page, on a successful logout it will automatically redirect 
    to the SplashScreen
   -->
  <p>Signout</p>
</template>

<script>
import { mapMutations } from 'vuex';

export default {
  name: 'Signout',
  // On create it removes local storage and wipes the vuex state
  created() {
    localStorage.removeItem('token');
    this.signOut();
    this.resetSettingsStore();
    this.$router.replace('/welcome');
  },
  methods: {
    ...mapMutations('auth', ['signOut']),
    ...mapMutations('settings', ['resetSettingsStore']),
  },
};
</script>

<!--  Script Chad found from google
https://developers.google.com/identity/sign-in/web/sign-in
<script>
  function signOut() {
    var auth2 = gapi.auth2.getAuthInstance();
    auth2.signOut().then(function () {
      console.log('User signed out.');
    });
  }
</script>
 -->

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
