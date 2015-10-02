%rebase base title='国信电商部 数据字典管理系统',position='数据字典管理',managetopli="active open",adduser="active"

<div class="page-body">
    <div class="row">
        <div class="col-lg-12 col-md-12 col-sm-12 col-xs-12">
            <div class="widget">
                <div class="widget-header bordered-bottom bordered-themesecondary">
                    <i class="widget-icon fa fa-tags themesecondary"></i>
                    <span class="widget-caption themesecondary">字典列表</span>
                    <div class="widget-buttons">
                        <a href="#" data-toggle="maximize">
                            <i class="fa fa-expand"></i>
                        </a>
                        <a href="#" data-toggle="collapse">
                            <i class="fa fa-minus"></i>
                        </a>
                        <a href="#" data-toggle="dispose">
                            <i class="fa fa-times"></i>
                        </a>
                    </div>
                    
                </div><!--Widget Header-->
                <div style="padding:-10px 0px;" class="widget-body no-padding">
                    <div class="tickets-container">
                        <div class="table-toolbar" style="float:left">
                            <a id="adddict" href="javascript:void(0);" class="btn  btn-primary ">
                                <i class="btn-label fa fa-plus"></i>添加数据字典
                            </a>
                            <a id="changedict" href="javascript:void(0);" class="btn btn-warning shiny">
                                <i class="btn-label fa fa-cog"></i>修改数据字典
                            </a>
                            <a id="deldict" href="javascript:void(0);" class="btn btn-darkorange">
                                <i class="btn-label fa fa-times"></i>删除数据字典
                            </a>
                        </div>
                       <table id="myLoadTable" class="table table-bordered table-hover"></table>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

<div class="modal fade" id="myModal" tabindex="-1" role="dialog"  aria-labelledby="myModalLabel" aria-hidden="true">
    <div class="modal-dialog" >
      <div class="modal-content" id="contentDiv">
         <div class="widget-header bordered-bottom bordered-blue ">
           <i class="widget-icon fa fa-pencil themeprimary"></i>
           <span class="widget-caption themeprimary" id="modalTitle">添加字典</span>
        </div>

         <div class="modal-body">
            <div>
            <form id="modalForm">
                <div class="form-group">
                  <label class="control-label" for="inputSuccess1">字段：</label>
                  <input type="text" class="form-control" id="dkey" name="dkey" require>
                </div>
                <div class="form-group">
                  <label class="control-label" for="inputSuccess1">含义：</label>
                  <input type="text" class="form-control" id="dvalue" name="dvalue" require>
                </div>
                <div class="form-group">
                  <label class="control-label" for="inputSuccess1">所在表：</label>
                  <input type="text" class="form-control" id="dtable" name="dtalble">
                </div>
                <div class="form-group">
                  <label class="control-label" for="inputSuccess1">说明：</label>
                  <input type="text" class="form-control" id="comment" name="comment">
                </div>
                <br></br>
                <input type="hidden" id="hidInput" value="">
                <button type="button" id="subBtn" class="btn btn-primary  btn-sm">提交</button>
                <button type="button" class="btn btn-warning btn-sm" data-dismiss="modal">关闭</button> 
             </form>
            </div>
         </div>
      </div>
   </div>
</div>
<script type="text/javascript">
$(function(){
    /**
    *表格数据
    */
    var editId;        //定义全局操作数据变量
	var isEdit;
	var modifyDKey;
	modifyDKey = '';
    $('#myLoadTable').bootstrapTable({
          method: 'post',
          url: '/api/getdict',
          contentType: "application/json",
          datatype: "json",
          cache: false,
          checkboxHeader: true,
          striped: true,
          pagination: true,
          pageSize: 15,
          pageList: [10,20,50],
          showColumns: true,
          search: true,
          showRefresh: true,
          minimumCountColumns: 2,
          clickToSelect: true,
          smartDisplay: true,
          //sidePagination : "server",
          sortOrder: 'desc',
          sortName: 'adddate',
          columns: [{
              field: 'bianhao',
              title: 'checkbox',      
              checkbox: true,
          },{
              field: 'dkey',
              title: '字段',
              align: 'center',
              valign: 'middle',
              sortable: true
          },{
              field: 'dvalue',
              title: '含义',
              align: 'center',
              valign: 'middle',
              sortable: true
          },{
              field: 'dtable',
              title: '所在表',
              align: 'center',
              valign: 'middle',
              sortable: true
          },{
              field: 'comment',
              title: '说明',
              align: 'center',
              valign: 'middle',
              sortable: true 
          },{
              field: 'adddate',
              title: '加入时间',
              align: 'center',
              valign: 'middle',
              sortable: true 
          }]
      });

    /**
    *添加弹出框
    */

	$('#adddict').click(function(){
        $('#modalTitle').html('添加字典');
        $('#hidInput').val('0');
        $('#myModal').modal('show');
        $('#modalForm')[0].reset();
        isEdit = 0;
    });


    /**
    *修改弹出框
    */

    $('#changedict').popover({
    	    html: true,
    	    container: 'body',
    	    content : "<h3 class='btn btn-danger'>请选择一条进行操作</h3>",
    	    animation: false,
    	    placement : "top"
    }).on('click',function(){
    		var result = $("#myLoadTable").bootstrapTable('getSelections');
    		if(result.length <= 0){
    			$(this).popover("show");
    			setTimeout("$('#changedict').popover('hide')",1000)
    		}
    		if(result.length > 1){
    			$(this).popover("show");
    			setTimeout("$('#changedict').popover('hide')",1000)
    		}
    		if(result.length == 1){
                $('#changedict').popover('hide');
                modifyDKey = result[0]['dkey'];
                $('#dkey').val(result[0]['dkey']);
                $('#dvalue').val(result[0]['dvalue']);
                $('#dtable').val(result[0]['dtable']);
                $('#comment').val(result[0]['comment']);
                $('#modalTitle').html('修改字典');     //头部修改
                $('#hidInput').val('1');            //修改标志
                $('#myModal').modal('show');
                editId = result[0]['dkey'];
				isEdit = 1;
    		}
        });

    /**
    *提交按钮操作
    */
    $("#subBtn").click(function(){
           var dkey = $('#dkey').val();
           if(modifyDKey!='')
           {
               if(dkey!=modifyDKey)
               {
                   $('#myModal').modal('hide');
                   message.message_show(200,200,'失败','不可修改字段值');
                   return false;
               }
               modifyDKey = ''
           }
           var dvalue = $('#dvalue').val();
           var dtable = $('#dtable').val();
           var comment = $('#comment').val();
           var postUrl;
           if(isEdit==1){
                postUrl = "/changedict/"+editId;           //修改路径
           }else{
                postUrl = "/adddict";          //添加路径
           }

           $.post(postUrl,{dkey:dkey,dvalue:dvalue,dtable:dtable,comment:comment},function(data){
                  if(data==0){
                    $('#myModal').modal('hide');
                    $('#myLoadTable').bootstrapTable('refresh');
                    message.message_show(200,200,'成功','添加成功');   
                  }else if(data==-1){
                      $('#myModal').modal('hide');
                      message.message_show(200,200,'失败','存在相同记录');
                      return false;
                      }
                  else if(data==2){
                    $('#myModal').modal('hide');
                    $('#myLoadTable').bootstrapTable('refresh');
                    message.message_show(200,200,'成功','修改成功');   
                  }else if(data==3){
                      $('#myModal').modal('hide');
                      message.message_show(200,200,'失败','修改失败');
                      return false;
                  }else{
                      $('#myModal').modal('hide');
                      message.message_show(200,200,'失败','异常状况');
                        console.log(data);return false;
                }
            },'html');
       });

        /**
        *删除按钮操作
        */        
    $('#deldict').popover({
                html: true,
                container: 'body',
                content : "<h3 class='btn btn-danger'>请选择要删除的记录</h3>",
                animation: false,
                placement : "top"
        }).on('click',function(){
            var res = $("#myLoadTable").bootstrapTable('getSelections');
            var str = '';
            if(res.length <= 0){
                $(this).popover("show");
                setTimeout("$('#deldict').popover('hide')",1000)
            }else{
                $(this).popover("hide");
                for(i in res){
                    str += res[i]['dkey']+',';
                }
                $.post('/deldict',{str:str},function(data){
                    if(data==0){
                        message.message_show(200,200,'删除成功',res.length+'条记录被删除');
                        $('#myLoadTable').bootstrapTable('refresh');
                    }else{
                        message.message_show(200,200,'失败','删除失败');
                    }
                },'html');  
                
            }
        });
        
})
</script>
