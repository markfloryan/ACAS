<template>
  <div class="question">
    <div class="questionText">
      <h4>{{select ? "Multiple Selection" : "Multiple Choice"}}</h4>
      <h5>{{question.question_parameters.question}}</h5>
    </div>
    <sui-form class="answers">
      <div v-for="(item, index) in question.question_parameters.choices" :key="index">
        <div class="ui checkbox" style="padding-top: 6pt">
          <input type="checkbox" name="answer">
          <label>{{String.fromCharCode(index + 65)}}) {{item.text}}</label>
        </div>
      </div>
    </sui-form>
    <div class="submit">
      <button
          class="btn btn-create edit-btn"
          style="float: right;"
          data-toggle="tooltip"
          data-placement="bottom"
          title="Submit"
          @click="submitQuestion()"
      >Submit</button>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { mapGetters, mapState, mapMutations } from 'vuex';
import { API_URL } from '@/constants';
import LoadingLayer from './LoadingLayer.vue';

export default {
  components: { LoadingLayer },
  data() {
    return {
      studentSelection: null,
    };
  },
  mounted() {
    console.log(this.question);
  },
  computed: {
    ...mapState('auth', ['profile']),
    ...mapGetters('settings', ['returnPrimaryButtonStyle']),
  },
  props: {
    select: {
      type: Boolean,
      required: true,
    },
    quiz: {
      type: Number,
      required: true,
    },
    question: {
      type: Object,
      require: true,
    }
  },
  methods: {
    ...mapMutations('toast', ['openToast', 'setToastInfo']),
    submitQuestion() {
      this.$emit('onSubmit');
      /*if(this.validate()){
        //CHANGE ALL OF THIS
        axios.post(`${API_URL}/quiz-questions/`,
          questionData,
          {
            headers: {
              Authorization: `Bearer ${this.profile.id_token}`
            }
          }
        ).then((response)=> {
          
        }).catch((error) => {
          if (error.response.data.status == '500 - Internal Server Error') {
            this.openToast();
            this.setToastInfo({
              type: 'error',
              title: '500 - Internal Server Error',
              message: `${error}`,
              duration: 10000,
            });
          } else {
            this.openToast();
            this.setToastInfo({
              type: 'error',
              title: 'Quiz Question Submission Error',
              message: `${error}`,
              duration: 10000,
            });
          }
        });
      }*/
    },
  },
};
</script>

<style scoped>
.question {
  display: grid;
  grid-template-areas:
      'questionText'
      'answers'
      'submit';
    grid-template-rows: auto auto auto;
}
.questionText {
  grid-area: questionText;
    padding-left: 10pt;
    padding-right: 10pt;
    padding-top: 10pt;
    padding-bottom: 10pt;
}
.answers {
  grid-area: answers;
    padding-left: 10pt;
    padding-right: 10pt;
}
.answer {
  grid-area: answer;
  display: grid;
  grid-template-areas:
      'label text';
    grid-template-columns: 1fr 20fr;
}
.label {
    grid-area: label;
    padding-left: 10pt;
    padding-right: 10pt;
    padding-top: 10pt;
    padding-bottom: 10pt;
    align-self: center;
}
.text {
    grid-area: text;
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