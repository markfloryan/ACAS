<template>
  <login-card isSignUp="true" />
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
