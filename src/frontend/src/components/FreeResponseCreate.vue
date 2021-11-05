<template>
  <div class="question">
    <div class="description">
      <h3>Free Response</h3>
      <p>A free response style question, intended to be used for numerical or very short answer questions. This question currently can only be autograded by a regular expression.</p>
    </div>
    <sui-form class="questionText">
        <sui-form-field>
          <label>Question Text</label>
          <input v-model="question" placeholder="Question" type="text">
        </sui-form-field>
    </sui-form>
    <sui-form class="answer">
      <sui-form-field>
        <label>Answer Regex</label>
        <input v-model="answer" placeholder="Regex" type="text">
      </sui-form-field>
    </sui-form>
    <div class="submit">
      <sui-form-field>
        <button
            class="btn btn-primary edit-btn"
            :style="returnPrimaryButtonStyle"
            style="float: right;"
            data-toggle="tooltip"
            data-placement="bottom"
            title="Add"
            @click="writeQuestion()"
        >Add Question</button>
      </sui-form-field>
    </div>
  </div>
</template>

<script>
import { mapGetters, mapState, mapMutations } from 'vuex';
import Dashboard from '../pages/Dashboard.vue';

export default {
  components: { Dashboard },
  data() {
    return {
      question: '',
      answer: '',
    };
  },
  mounted() {
  },
  computed: {
    ...mapState('auth', ['profile']),
    ...mapGetters('settings', ['returnPrimaryButtonStyle']),
  },
  props: {
  },
  methods: {
    ...mapMutations('toast', ['openToast', 'setToastInfo']),
    validate() {
      if (this.question == '') {
        this.openToast();
        this.setToastInfo({
          type: 'error',
          title: 'Error',
          message: 'Question text empty.',
          duration: 10000,
        });
        return false;
      }

      if (this.answer == '') {
        this.openToast();
        this.setToastInfo({
          type: 'error',
          title: 'Error',
          message: 'Answer regex empty.',
          duration: 10000,
        });
        return false;
      }
      
      return true;
    },
    writeQuestion() {
      if(this.validate()){
        this.openToast();
        this.setToastInfo({
          type: 'success',
          title: 'Success',
          message: 'Added question',
          duration: 10000,
        });
      }
    }
  },
};
</script>

<style scoped>
.question {
  display: grid;
  grid-template-areas:
      'description'
      'questionText'
      'answer' 
      'submit';
    grid-template-rows: auto auto auto auto;
}
.description {
  grid-area: description;
  padding-left: 10pt;
  padding-right: 10pt;
  padding-top: 10pt;
  padding-bottom: 10pt;
}
.questionText {
  grid-area: questionText;
    padding-top: 10pt;
    padding-bottom: 10pt;
    padding-left: 10pt;
    padding-right: 10pt;
}
.answer {
  grid-area: answer;
    padding-left: 10pt;
    padding-right: 10pt;
    padding-top: 10pt;
    padding-bottom: 10pt;
}
.submit {
    grid-area: submit;
    padding-left: 10pt;
    padding-right: 10pt;
    padding-top: 10pt;
    padding-bottom: 10pt;
}
</style>