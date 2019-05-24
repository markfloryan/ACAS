<template>
  <!-- SplashScreen.vue
    This is the main screen unlogged users are jumped to and has the login / signup flow in it 
   -->
  <login-card />
</template>

<script>
import LoginCard from '@/components/LoginCard';

export default {
  name: 'SplashScreen',

  components: {
    LoginCard,
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  .login-card {
    height: 150pt;
    width: 300pt;
    margin: auto;
    margin-top: 25vh !important;
  }
</style>
