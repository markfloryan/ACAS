<template>
  <div class="loading-layer">
    <!-- LoadingLayer.vue
      This is a helper component that you can through in to other components
      to conditional show a loading animation and obscure/disable the 
      funtionality of the parent component

      To use: include in the parent component
       <LoadingLayer v-if="loading" />

      Where 'loading' is the var determining whether something is loading or not.
      When loading is true, this component will be visible and show the loading animation
      else: it will be invisible
     -->
    <sui-icon name="spinner" size="huge" loading class="loading-icon"/>
    <p v-if="message" class="message">
      {{ message }}
    </p>
  </div>
</template>

<script>

export default {
  name: 'LoadingLayer',

  components: {
    
  },
  props: {
    // You can pass in a prop 'message' which is the text shown under the loading animation
    message: {
      type: String,
      default: 'Loading...',
    }
  },
};
</script>


<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  .loading-layer {
    background-color: rgba(255, 255, 255, 0.8);
    width: 100%;
    height: 100%;
    position: absolute;
    top: 0;
    left: 0;
    
    display: grid;
    grid-template-areas: 
    '.'
    'icon'
    'message'
    '.';
    grid-template-rows: 1fr min-content min-content 1fr;
  }
  .loading-layer > .loading-icon {
    grid-area: icon;
    margin: auto;
  }
  .loading-layer > .message {
    grid-area: message;
    text-align: center;
    padding: 27pt;
    font-size: 13.5pt;
  }
</style>
