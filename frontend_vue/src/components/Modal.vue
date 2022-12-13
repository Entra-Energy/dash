<template>
    <button type="button" class="btn btn-primary" data-toggle="modal" data-target="#exampleModal">
  Launch
    </button>



    <div class="modal fade" id="exampleModal" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel" aria-hidden="true">
  <div class="modal-dialog" role="document">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title" id="exampleModalLabel">Modal title</h5>
        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
          <span aria-hidden="true">&times;</span>
        </button>
      </div>
      <div class="modal-body">
        
        <li v-for="flex in flexi">
            {{mydev}}
  {{flex.dev}}
</li>
        
       
        <ul>
               <!-- <li v-for="flex in flexi" :key="mydev">
                {{mydev}}
                 <span v-if="flexi.dev === mydev">{{flexi.dev}}</span> 

               </li> -->
        </ul>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
        <button type="button" class="btn btn-primary">Save changes</button>
      </div>
    </div>
  </div>
</div>
</template>
  <script>
  
  export default {
    name: "Modal",
    props: {
    flexi: [],
    mydev:[],
    
    
  },
    data() {
      return {
 
        
      };
    },
    methods: {
        
        findLog(){
        
          
        }
   
  
    },
    created(){
           this.findLog()
      
    },
    
  };
  </script>
  
  <style scoped>
  
  </style>
  