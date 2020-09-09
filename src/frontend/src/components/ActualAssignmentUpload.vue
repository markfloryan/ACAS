<template>
    <div class="container">
        <div class="large-12 medium-12 small-12 cell" style="padding:10px">
        <h3>Upload assignments</h3>
        <p>This upload creates an assignment or does nothing if it already exists. CSV Schema: assignment_name, topic_name</p>
        <label>
            <input type="file" id="file2" ref="file2" v-on:change="handleAssignmentFileUpload()"/>
        </label>
            <button v-on:click="submitAssignmentFile()">Upload</button>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
import { mapGetters, mapState, mapMutations } from 'vuex';
import { API_URL } from '@/constants';
export default {
  /*
  Defines the data used by the component
  */
  data(){
    return {
      file: ''
    };
  },
  props: {
    courseId: {
      type: String,
      required: true,
    }
  },
  computed: {
    ...mapState('auth', ['profile']),
  },
  methods: {
    ...mapMutations('toast', ['openToast', 'setToastInfo']),
    handleAssignmentFileUpload() {
      this.file2 = this.$refs.file2.files[0];
    },
    submitAssignmentFile(){
      let formData = new FormData();
      formData.append('csv', this.file2);
      
      
      
      //let formattedURL = `${API_URL}/courseAssignmentUpload/${this.pk}`;
      
      /*.get(
          `${API_URL}/student/course/?courseId=${
            this.id
          }&view_as=${viewAs}&id_token=${this.profile.id_token}`
      )*/
      let localID = this.profile.id_token;
      let coursePK = this.courseId;
      axios
        .post( `${API_URL}/courseAssignmentUpload/${coursePK}`,
          formData,
          {
            headers: {
              'Content-Type': 'multipart/form-data',
              Authorization: `Bearer ${this.profile.id_token}`
            }
          }
        ).then((response)=> {
          //for (i=0; i<response.data.errors.length; i++) {
          if(response.data.ok) {
            this.openToast();
            this.setToastInfo({
              type: 'success',
              title: 'Successful Upload',
              message: 'Assignments added to gradebook',
              duration: 5000,
            });
          }
          else {
            this.openToast();
            this.setToastInfo({
              type: 'error',
              title: 'Uploading Error',
              message: `${response.data.errors}`,
              duration: 10000,
            });
          }
        /*
        setTimeout(function(){ 
          openToast();
          this.setToastInfo({
            type: 'error',
            title: 'Uploading Error',
            message: `${response.data.errors[1]}`,
            duration: 6000,
        }); }, 6000);*/
          //}
      
        })
        .catch(function(){
          console.log(`${API_URL}/courseAssignmentUpload/${coursePK}`);
          console.log('FAILURE');
        });
    }
  } 
};
</script>
