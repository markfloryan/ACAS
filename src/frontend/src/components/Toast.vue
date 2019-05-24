<template>
  <div class="toast-container">
    <transition name="slide-fade">
      <div v-if="visible" class="toast" :style="toastStyle">
        <h3 class="toast-title">{{ title }}</h3>
        <sui-icon class="toast-close" name="close icon" @click="closeToast"/>
        <p v-if="message" class="toast-message">{{ message }}</p>
      </div>
    </transition>
  </div>
</template>

<script>
import { mapState, mapMutations } from 'vuex';

export default {
  computed: {
    toastStyle() {
      let backgroundColor = 'white';
      let borderLeft = 'var(--color-blue-40) 6pt solid';

      if (this.type === 'success') {
        backgroundColor = 'var(--color-green-10)';
        borderLeft = 'var(--color-green-40) 6pt solid';
      }
      else if (this.type === 'error') {
        backgroundColor = 'var(--color-red-10)';
        borderLeft = 'var(--color-red-30) 6pt solid';
      }

      return {
        'background-color': backgroundColor,
        'border-left': borderLeft,
      };
    },
    ...mapState({
      message: state => state.toast.message,
      title: state => state.toast.title,
      type: state => state.toast.type,
      visible: state => state.toast.visible,
      duration: state => state.toast.duration,
    }),
  },
  updated() {
    if (this.visible) {
      setTimeout(() => {
        this.closeToast();
      }, this.duration);
    }
  },
  methods: {
    ...mapMutations('toast', ['closeToast']),
  },
};
</script>

<style>
  .toast-container {
    z-index: 10000000;
    position: fixed;
    right: 6pt;
    bottom: 6pt;
  }
  .toast {
    width: 225pt;
    border-radius: 3pt;
    padding: 8pt;
    

    display: grid;
    grid-template-areas:
    'title close'
    'message message';
    grid-template-columns: 1fr min-content;
    grid-template-rows: min-content 1fr;
  }
  .toast > .toast-title { grid-area: title; margin-bottom: 0pt;}
  .toast > .toast-close { 
    grid-area: close;
    cursor: pointer;
  }
  .toast > .toast-close:hover { color: var(--color-blue); }
  .toast > .toast-message { 
    grid-area: message;
    margin-top: 3pt;
  }

  .slide-fade-enter-active {
    transition: all 0.5s ease;
  }
  .slide-fade-leave-active {
    transition: all .5s ease;
  }
  .slide-fade-enter, .slide-fade-leave-to
  /* .slide-fade-leave-active below version 2.1.8 */ {
    transform: translateX(225pt);
    opacity: 0;
  }
</style>