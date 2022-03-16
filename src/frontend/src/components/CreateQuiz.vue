<template>
    <div>
        <div class="quizCreator" v-if="quiz == null">
            <div class="title" style="padding:10px">
                <h3>Create a quiz!</h3>
            </div> 
            <div class="content">
                <h4>Select a Topic</h4>
                <sui-form-field>
                    <sui-dropdown
                    placeholder="Select topic"
                    :options="topics"
                    selection
                    search
                    v-model="topicPK"
                    />
                </sui-form-field>
                <h4 v-if="topicPK !== null">Select an Assignment</h4>
                <sui-form-field>
                    <sui-dropdown
                        placeholder="Select assignment"
                        v-if="topicPK !== null"
                        :options="assignments"
                        selection
                        search
                        v-model="assignment"
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
                    title="Create Quiz"
                    @click="saveQuiz()"
                >Create Quiz</button>
            </div>
        </div>
        <div v-if="quiz !== null">
            <QuestionWriter :quiz="quiz"></QuestionWriter>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
import { mapGetters, mapState, mapMutations } from 'vuex';
import { API_URL } from '@/constants';
import QuestionWriter from '@/components/QuestionWriter';

export default {
  components: { QuestionWriter },
  /*
  Defines the data used by the component
  */
  data(){
    return {
      topics: [],
      topicPK: null,
      assignments: [],
      assignment: null,
      quiz: null,
    };
  },
  mounted() {
    this.getTopics();
    if(this.topicId) {
      this.topicPK = this.topicId;
    }
  },
  watch: {
    topicPK: function (){
      this.getAssignments(this.topicPK);
    }
  },
  props: {
    courseId: {
      type: String,
      required: true,
    },
    topicId: {
      type: Number,
      required: false,
    }
  },
  computed: {
    ...mapState('auth', ['profile']),
    ...mapGetters('settings', ['returnPrimaryButtonStyle']),
  },
  methods: {
    ...mapMutations('toast', ['openToast', 'setToastInfo']),
    validate() {
      return this.topicPK != null && this.assignment != null;
    },
    getAssignments() {
      axios.get(`${API_URL}/assignments/?topicId=${this.topicPK}`, 
        { 
          headers: {
            'Content-Type': 'multipart/form-data',
            Authorization: `Bearer ${this.profile.id_token}`
          }
        }).then((response)=> {
        let data = response.data.result;
        this.assignments = [];
        for(let i=0;i<data.length;i++){
          let assignment = data[i];
          this.assignments.push({
            text: assignment.name,
            value: assignment.pk
          });
        }
      }).catch(function(){

      });
    },
    getTopics() {
      axios.get(`${API_URL}/topics/?courseId=${this.courseId}`, 
        { 
          headers: {
            'Content-Type': 'multipart/form-data',
            Authorization: `Bearer ${this.profile.id_token}`
          }
        }).then((response)=> {
        let data = response.data.result;
        for(let i=0;i<data.length;i++){
          let topic = data[i];
          this.topics.push({
            text: topic.name,
            value: topic.pk
          });
        }
      }).catch(function(){

      });
    },
    saveQuiz() {
      if(this.validate()) {
        let now = new Date(Date.now());
        let quizData = {
          quizzes: [{
            pk: 'None',
            assignment: this.assignment,
            next_open_date: now.toISOString(),
            next_close_date: now.toISOString(),
          },]
        };

        axios.post(`${API_URL}/quizzes/`,
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
              title: 'Successful Creation',
              message: 'Quiz successfully created',
              duration: 5000,
            });
            axios.get(`${API_URL}/quizzes/`,{
              headers: {
                Authorization: `Bearer ${this.profile.id_token}`
              },
            }
            ).then((response) => {
              this.quiz = response.data.result[response.data.result.length - 1].pk;
            });
          }
          else {
            this.openToast();
            this.setToastInfo({
              type: 'error',
              title: 'Creation Error testing',
              message: `${response.data.errors}`,
              duration: 10000,
            });
          }
        }).catch((error) => {
          if(error.response.data.status == '400 - Bad Request') {
            if(error.response.data.missing_data.assignment){
              this.openToast();
              this.setToastInfo({
                type: 'error',
                title: 'Assignment',
                message: `${error.response.data.missing_data.assignment[0]} This quiz already exists`,
                duration: 10000,
              });
            } else {
              this.openToast();
              this.setToastInfo({
                type: 'error',
                title: '400 - Bad Request',
                message: `${error}`,
                duration: 10000,
              });
            }
          } else if (error.response.data.status == '500 - Internal Server Error') {
            this.openToast();
            this.setToastInfo({
              type: 'error',
              title: '500 - Internal Server Error',
              message: `${error}`,
              duration: 10000,
            });
          }
        });
      } else {
        this.openToast();
        this.setToastInfo({
          type: 'error',
          title: 'Missing Data',
          message: 'One or more fields are empty',
          duration: 10000,
        });
      }
    }
  }
};
</script>


<style scoped>
.quizCreator {
    display: grid;
    grid-template-areas:
        'title'
        'content'
        'buttons';
    grid-template-columns: 1fr;
    grid-template-rows: 1 8 1;
}
.title {
    grid-area: title;
    padding: 10pt;
}
.buttons {
    grid-area: buttons;
    padding: 10pt;
}
.content {
    grid-area: content;
    padding: 10pt;
}
</style>
