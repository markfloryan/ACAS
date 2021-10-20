<template>
    <div class="questionCreator">
        <div class="title" style="padding:10px">
          <h3>Add a Question</h3>
        </div>
        <div class="content">
          <sui-form-field>
            <sui-dropdown
                placeholder="Select type of question"
                :options="questionTypes"
                selection
                search
                v-model="questionPK"
            />
          </sui-form-field>
        </div>
        <div class="buttons">
          <button
              class="btn btn-primary edit-btn"
              :style="returnPrimaryButtonStyle"
              style="float: right;"
              data-toggle="tooltip"
              data-placement="bottom"
              title="Add"
              @click="writeQuestion()"
          >Add Question</button>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
import { mapGetters, mapState, mapMutations } from 'vuex';
import { API_URL } from '@/constants';
import Dashboard from '../pages/Dashboard.vue';

export default {
  components: { Dashboard},
  /*
  Defines the data used by the component
  */
  data(){
    return {
      questionTypes: [],
      questionPK: null,
    };
  },
  mounted() {
    this.questionTypes = [{text: 'Multiple Choice', value: 0}, {text: 'Multiple Select', value: 1}, {text: 'Free Response', value: 2}, {text: 'Coding', value: 3}, {text: 'Custom', value: 4}];
  },
  watch: {
  },
  props: {
    topicPK: {
      type: Number,
      required: true,
    },
    assignmentPK: {
      type: Number,
      required: true,
    }
  },
  computed: {
    ...mapState('auth', ['profile']),
    ...mapGetters('settings', ['returnPrimaryButtonStyle']),
  },
  methods: {
    ...mapMutations('toast', ['openToast', 'setToastInfo']),
    validate() {

    },
    writeQuestion() {
      this.openToast();
      this.setToastInfo({
        type: 'error',
        title: 'Error',
        message: 'Not Implemented Yet',
        duration: 10000,
      });
    }
  } 
};
</script>

<style scoped>
.questionCreator {
    display: grid;
    grid-template-areas:
        'title'
        'content'
        'buttons';
    grid-template-columns: 1fr;
    grid-template-rows: 1fr 8fr 1fr;
}
.title {
    grid-area: title;
    padding-left: 10pt;
    padding-right: 10pt;
}
.buttons {
    grid-area: buttons;
    padding-left: 10pt;
    padding-right: 10pt;
}
.content {
    grid-area: content;
    padding-left: 10pt;
    padding-right: 10pt;
}
</style>