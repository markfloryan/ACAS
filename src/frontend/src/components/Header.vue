<template>
  <!-- Header.vue
    This is the header at the top of every page on the website
    It can dynamically change its look based on whether a user is logged in or not
  -->
  <div class="menu-container" :style="{
    backgroundColor: 'linear-gradient(#FFF,#000)',
    background: 'linear-gradient(#FFF 90%,'+hexToRgbA(returnColor)+')',
    height:'4rem%',
    'border-top':'3.75pt #fff',
  }">
    <div class="menu">

      <div class="left">
        <search-field
          v-if="isAuthenticated && profile.group"
          :placeholder="'Search students...'"
          @pass-data="searchValue"/>
        <template v-else>
          <router-link v-if="false" to="/about" class= "about">About</router-link>
          <router-link v-if="false" to="/contact" class = "contact-us">Contact us</router-link>
        </template>
      </div>
      <div class="middle">
        <router-link to="/" class="logo">
          <img
            width="25px"
            height="25px"
            src="../assets/logo_transparent_2.png" />
        </router-link>
      </div>
      <div class="right">
        <router-link v-if="!isAuthenticated" to="/welcome" class="login">Login</router-link>

        <template v-else>
          <ViewAsWidget class="view-as-widget"
            :viewingAsId="$route.query.viewAs"/>
          <router-link to="/settings"> Settings </router-link>
          <router-link to="/signout">Signout</router-link>
        </template>
      </div>
    </div>
  </div>
</template>

<script>
import SearchField from '@/components/SearchField';
import ViewAsWidget from '@/components/ViewAsWidget';
import { mapGetters, mapState } from 'vuex';
import store from '../vuex';

export default {
  name: 'Header',
  components: {
    SearchField,
    ViewAsWidget,
  },
  props: {
    role: {
      type: String,
      default: 'Student' // valid values: ['Student', 'Professor']
    }
  },
  data() {
    return {
      inputFocused: false,
      names: 'lol',
    };
  },
  computed: {
    // This is the var that determines whether to render logged in or logged out header
    isAuthenticated() {
      return this.$store.state.auth.signedIn;
    },
    ...mapState('auth', ['profile']),
    ...mapGetters(
      'settings', ['returnColor'],
      'settings', ['returnNickName'],
    ),
  },
  methods: {
    setFocus: value => {
      this.inputFocused = value;
    },
    // Right now this is dummy function that gets called when a user presses enter on
    // the search bar or clicks the search icon in the search bar
    searchValue(value) {
      this.$router.push({
        name: 'Search',
        params: { query: encodeURIComponent(value) },
      });
    },
    hexToRgbA(hex){
      let c;
      if(/^#([A-Fa-f0-9]{3}){1,2}$/.test(hex)){
        c = hex.substring(1).split('');
        if(c.length== 3){
          c= [c[0], c[0], c[1], c[1], c[2], c[2]];
        }
        c = '0x'+c.join('');
        return `rgba(${[(c>>16)&255, (c>>8)&255, c&255].join(',')} ,1)`;
      }
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.menu-container {
   background-color: #fff;
  width: 100%;
  position: fixed;
  top: 0;
  -webkit-box-shadow: 0 0.75pt 1.5pt 0 rgba(34, 36, 38, 0.15);
  box-shadow: 0 0.75pt 1.5pt 0 rgba(34, 36, 38, 0.15);
  border: 0.75pt solid rgba(34, 36, 38, 0.15);
  z-index: 10000000000;
}
.menu {
  max-width: 1290pt;
  margin: auto;
  padding: 5.25pt 2vw;
  display: grid;
  grid-template-areas: 'left middle right';
  grid-template-columns: 1fr 1fr 1fr;
}
.left {
  grid-area: left;
  text-align: left;
}
.right {
  grid-area: right;
  text-align: right;
}
.middle {
  grid-area: middle;
  text-align: center;
}

.menu a:not(.logo), .view-as-widget {
  display: inline-block;
  position: relative;
  top: 50%;
  transform: perspective(0.75pt) translateY(-50%);
  padding: 0pt 8pt;
}

.menu a:not(.logo):hover {
  color: dodgerblue;
}

.menu a {
  color: #000;
  vertical-align: middle;
}

.right a:last-child {
  padding: 0pt 0pt 0pt 8pt;
}
.left a:first-child {
  padding: 0pt 8pt 0pt 0pt;
}
</style>
