<template>
  <div>
    <div class="quiz" v-if="!edittingQuestion && !newQuestion">
      <div class="title" style="padding:10px">
        <h3>{{assignmentQuizPair.assignment.name}}</h3>
        <button @click="deleteQuiz(assignmentQuizPair.quiz)" class="btn btn-delete" style="float: right" type="button">Delete Quiz</button>
        <p>Status: {{assignmentQuizPair.quiz.published ? "Published" : "Unpublished"}}</p>
      </div>
      <div class="table">
        <sui-table v-if="questions.length > 0" celled>
          <sui-table-header>
            <sui-table-row>
              <sui-table-header-cell :width="3">Question</sui-table-header-cell>
              <sui-table-header-cell :width="1">Type</sui-table-header-cell>
              <sui-table-header-cell :width="2">Actions</sui-table-header-cell>
            </sui-table-row>
          </sui-table-header>
          <sui-table-body>
            <sui-table-row
              v-for="question in questions" v-bind:key="question.pk"
            >
              <sui-table-cell>{{ question.question_parameters.question }}</sui-table-cell>
              <sui-table-cell v-if="question.question_type === 0">Multiple Choice</sui-table-cell>
              <sui-table-cell v-if="question.question_type === 1">Multiple Select</sui-table-cell>
              <sui-table-cell v-if="question.question_type === 2">Free Response</sui-table-cell>
              <sui-table-cell v-if="question.question_type === 3">Coding</sui-table-cell>
              <sui-table-cell v-if="question.question_type === 4">Execution</sui-table-cell>
              <sui-table-cell>
                <center>
                  <button @click="editQuestion(question)" class="btn btn-primary" type="button">Edit</button>
                  <button @click="deleteQuestion(question)" class="btn btn-delete" type="button">Delete</button>
                </center>
              </sui-table-cell>
            </sui-table-row>
          </sui-table-body>
        </sui-table>
      </div>
      <div class="buttons">
        <button v-if="!assignmentQuizPair.quiz.published" @click="publish()" class="btn btn-primary" style="float: left" type="button">Publish Quiz</button>
        <button v-if="assignmentQuizPair.quiz.published" @click="unpublish()" class="btn btn-delete" style="float: left" type="button">Unpublish Quiz</button>
        <button @click="createQuestion()" class="btn btn-create" style="float: right" type="button">New Question</button>
      </div>
    </div>
    <div v-if="questionSelection !== null">
      <MultipleChoiceCreate 
        v-if="edittingQuestion && questionSelection.question_type===0 || questionSelection.question_type===1" 
        :select="questionSelection.question_type===1" 
        :quiz="assignmentQuizPair.quiz.pk" 
        :question="questionSelection"
        @onClose="refreshEditor()" />
    </div>
    <div v-if="newQuestion">
      <QuestionWriter
        :quiz="assignmentQuizPair.quiz.pk"
        :fromEdit="true"
        @onClose="refreshEditor()"/>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { mapGetters, mapState, mapMutations } from 'vuex';
import { API_URL } from '@/constants';
import QuestionWriter from '@/components/QuestionWriter';
import MultipleChoiceCreate from '@/components/MultipleChoiceCreate';

export default {
  components: { 
    QuestionWriter,
    MultipleChoiceCreate
  },
  /*
  Defines the data used by the component
  */
  data(){
    return {
      questions: [],
      questionSelection: null,
      edittingQuestion: false,
      newQuestion: false,
    };
  },
  mounted() {
    this.getQuestions();
  },
  watch: {
  },
  props: {
    courseId: {
      type: String,
      required: true,
    },
    assignmentQuizPair: {
      type: Object,
      required: true,
    }
  },
  computed: {
    ...mapState('auth', ['profile']),
    ...mapGetters('settings', ['returnPrimaryButtonStyle']),
  },
  methods: {
    ...mapMutations('toast', ['openToast', 'setToastInfo']),
    getQuestions() {
      axios.get(`${API_URL}/quiz-questions/?quiz=${this.assignmentQuizPair.quiz.pk}&mode=practice`, 
        { 
          headers: {
            'Content-Type': 'multipart/form-data',
            Authorization: `Bearer ${this.profile.id_token}`
          }
        }).then((response)=> {
        this.questions = response.data.result;
        this.questions.forEach(question => {
          question.question_parameters = JSON.parse(question.question_parameters);
        });
      }).catch(function(){

      });
    },
    refreshEditor() {
      this.edittingQuestion = false;
      this.newQuestion = false;
      this.questionSelection = null;
      this.getQuestions();
    },
    editQuestion(question) {
      this.edittingQuestion = true;
      this.questionSelection = question;
    },
    deleteQuestion(question) {
      axios
        .delete(`${API_URL}/quiz-questions/${question.pk}`, { headers: { Authorization: `Bearer ${this.profile.id_token}` } })
        .then(response => {
          if(response.status == 200)
            this.getQuestions();
        })
        .catch(error => {
          console.log(error);
        });
    },
    publish() {
      let now = new Date(Date.now());
      let quizData = {
        pk: this.assignmentQuizPair.quiz.pk,
        assignment: this.assignmentQuizPair.quiz.assignment,
        published: true,
        next_open_date: now.toISOString(),
        next_close_date: now.toISOString(),
      };

      axios.put(`${API_URL}/quizzes/${this.assignmentQuizPair.quiz.pk}`,
        quizData,
        {
          headers: {
            Authorization: `Bearer ${this.profile.id_token}`
          }
        }
      ).then((response)=> {
        if(response.data.status == '200 - OK') {
          this.openToast();
          this.setToastInfo({
            type: 'success',
            title: 'Successful publish',
            message: 'Quiz successfully published',
            duration: 5000,
          });
          this.$emit('onClose');
        }
      }).catch((error) => {
        this.openToast();
        this.setToastInfo({
          type: 'error',
          title: 'Failed to publish',
          message: 'Quiz failed to publish',
          duration: 5000,
        });
      });
    },
    unpublish() {
      let now = new Date(Date.now());
      let quizData = {
        pk: this.assignmentQuizPair.quiz.pk,
        assignment: this.assignmentQuizPair.quiz.assignment,
        published: false,
        next_open_date: now.toISOString(),
        next_close_date: now.toISOString(),
      };

      axios.put(`${API_URL}/quizzes/${this.assignmentQuizPair.quiz.pk}`,
        quizData,
        {
          headers: {
            Authorization: `Bearer ${this.profile.id_token}`
          }
        }
      ).then((response)=> {
        if(response.data.status == '200 - OK') {
          this.openToast();
          this.setToastInfo({
            type: 'success',
            title: 'Successful unpublish',
            message: 'Quiz successfully unpublished',
            duration: 5000,
          });
          this.$emit('onClose');
        }
      }).catch((error) => {
        this.openToast();
        this.setToastInfo({
          type: 'error',
          title: 'Failed to unpublish',
          message: 'Quiz failed to unpublish',
          duration: 5000,
        });
      });
    },
    createQuestion() {
      this.newQuestion = true;
    },
    deleteQuiz(quiz) {
      axios
        .delete(`${API_URL}/quizzes/${quiz.pk}`, { headers: { Authorization: `Bearer ${this.profile.id_token}` } })
        .then(response => {
          if(response.status == 200)
            this.$emit('onClose');
        })
        .catch(error => {
          console.log(error);
        });
    },
  }
};
</script>


<style scoped>
.quiz {
    display: grid;
    grid-template-areas:
        'title'
        'table'
        'buttons';
    grid-template-columns: 1fr;
    grid-template-rows: 1 1 1;
    padding: 10pt;
}
.title {
    grid-area: title;
    padding: 10pt;
}
.table {
    grid-area: table;
}
.buttons {
    grid-area: buttons;
    padding: 10pt;
}
</style>
