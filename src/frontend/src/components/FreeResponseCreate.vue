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
import axios from 'axios';
import { mapGetters, mapState, mapMutations } from 'vuex';
import { API_URL } from '@/constants';
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
    quiz: {
      type: Number,
      required: true,
    },
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
        let questionData = {
          'quiz-questions': [{
            pk: 'None',
            quiz: this.quiz,
            question_type: 2,
            answered_correct: 0,
            answered_total: 0,
            question_parameters: JSON.stringify({
              question: this.question,
              answer: this.answer
            })
          }]
        };
        axios.post(`${API_URL}/quiz-questions/`,
          questionData,
          {
            headers: {
              Authorization: `Bearer ${this.profile.id_token}`
            }
          }
        ).then((response)=> {
          console.log(response.data);
          if(response.data.status == '200 - OK') {
            this.openToast();
            this.setToastInfo({
              type: 'success',
              title: 'Successful Creation',
              message: 'Question successfully added',
              duration: 5000,
            });
            this.$emit('onClose');
          }
          else {
            this.openToast();
            this.setToastInfo({
              type: 'error',
              title: 'Creation Error',
              message: `${response.data.errors}`,
              duration: 10000,
            });
          }
        }).catch(function(){
          console.log('Question writing failure');
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