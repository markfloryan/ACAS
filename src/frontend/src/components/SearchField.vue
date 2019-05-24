<template>
  <!-- SearchField.vue
    This is the search field that is conditionally shown in the Header.vue component

    This compoenent just acts as a pretty container and doesn't actually handle
    searching itself, it only captures the input (search text) and sends it to the parent 
    when the enter key is pressed or the search icon is pressed,
    to do something with this search text, place a method in parent component
    and pass that function, pass it to the pass-data emitted event like:
    <SearchField @pass-data="FUNCTION_TO_BE_EXECUTED" />
   -->
  <div class="search-input" :style="{
    'background-color': inputFocused ? 'white' : null,
    'border': inputFocused ? '0.75pt solid dodgerblue' : null,
    'width': width,
  }">
    <input
      @focus="inputFocused = true"
      @blur="inputFocused = false"
      @keyup.enter="sendData"
      v-model="value"
      class="search-field"
      :placeholder="placeholder" />
    <sui-icon
      @click="sendData"
      class="search-icon"
      name="search" />
  </div>
</template>

<script>
export default {
  name: 'SearchField',
  props: {
    placeholder: {
      type: String,
      default: 'Search...',
    },
    width: {
      type: String,
      default: '225pt',
    },
  },
  data() {
    return {
      inputFocused: false,
      value: '',
    };
  },
  methods: {
    // emits the 'pass-data event to the parent and sends over the search text (this.value)
    sendData() {
      this.value = this.value ? this.value : 'All';
      this.$emit('pass-data', this.value);
    },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  .search-input {
    display: inline-block;
    position: relative;
    top: 50%;
    transform: perspective(0.75pt) translateY(-50%);
    border-radius: 30pt;
    height: 24pt;
    background-color: #F0F3F5;
    border: 0.75pt solid #CCC;
    padding: 4.5pt 8pt;        /* Opera/IE 8+ */
  }
  .search-input input {
    border: none;
    background-color: transparent;
    font-size: 8pt;
    outline: none;
    width: 80%;
  }
  .search-icon {
    float: right;
    cursor: pointer;
  }
</style>
