<template>
    <transition name="fade">
        <div v-if="isSaved" class="saved">
            <div class="content">
            <h1>*Saved*</h1>
            </div>
        </div>
    </transition>
</template>

<script>
//Displays Saved 
import axios from 'axios';
import { API_URL } from '@/constants';

export default {
  name: 'Saved',
  components: {
  },
  props: {
    isSaved: {
      type: Boolean,
      required: false,
    },
  },
  watch:{
    isSaved: function(){
    //   this.isSaved = false;
    },
  },

  data() {
    return {
    };
  },
  mounted() {},
  created() {
  },
  updated() {},
  methods: {
    closeSaved(event) {
      this.$emit('onCloseSave');
    },
  },
};
</script>

<style scoped>
.tab-nav {
  padding-bottom: 8pt;
  margin-bottom: 8pt;
  border-bottom: var(--color-green-10) 0.75pt solid;
}
.tab-nav .link {
  font-weight: bold;
  font-size: 12pt;
  margin-right: 8pt;
  cursor: pointer;
}
.topic-modal {
  position: absolute;
  top: 0;
  left: 0;
  z-index: 1000000;
  width: 100%;
  height: 100%;
  border-radius: 6pt;
  background-color: rgba(100, 100, 100, 0.8);
}
.topic-modal > .content {
  grid-area: content;

  background-color: #fff;
  -webkit-box-shadow: 0 0.75pt 1.5pt 0 rgba(34, 36, 38, 0.15);
  box-shadow: 0 0.75pt 1.5pt 0 rgba(34, 36, 38, 0.15);
  border: 0.75pt solid rgba(34, 36, 38, 0.15);
  padding: 8pt;
  border-radius: 6pt;

  margin: auto;
  width: 70%;
  min-width: 525pt;
  height: 95%;

  position: relative;
  top: 50%;
  transform: perspective(0.75pt) translateY(-50%);
  padding: 18pt;

  display: grid;
  grid-template-areas:
    'title exit'
    'tabnav tabnav'
    'main main';
  grid-template-rows: min-content min-content 1fr;
  grid-template-columns: 1fr min-content;
}

.topic-modal > .content > .title {
  grid-area: title;
}
.topic-modal > .content > .tab-nav {
  grid-area: tabnav;
}
.topic-modal > .content > .main {
  grid-area: main;
}

.close-modal-button {
  cursor: pointer;
  grid-area: exit;
}
.close-modal-button:hover {
  color: var(--color-blue);
}
.main {
  height: 50pt;
}

.fade-enter-active, .fade-leave-active {
  transition: opacity .5s;
}
.fade-enter {
  opacity: 1;
}
.fade-enter-to, .fade-leave-to /* .fade-leave-active below version 2.1.8 */ {
  opacity: 0;
}
</style>
