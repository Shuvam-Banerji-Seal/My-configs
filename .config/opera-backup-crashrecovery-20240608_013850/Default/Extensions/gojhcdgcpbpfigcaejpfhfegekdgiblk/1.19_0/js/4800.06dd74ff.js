"use strict";(self["webpackChunkdesktop_wallet"]=self["webpackChunkdesktop_wallet"]||[]).push([[4800],{90881:function(t,e,s){s.d(e,{Z:function(){return d}});var i=function(){var t=this,e=t._self._c;return e("transition",{attrs:{name:"fade"}},[e("div",{directives:[{name:"show",rawName:"v-show",value:t.showing,expression:"showing"}],staticClass:"bg-black bg-opacity-40 bottom-0 fixed flex items-center justify-center left-0 right-0 top-0 z-10"},[e("div",{staticClass:"bg-modal flex flex-col items-center max-w-screen-sm mx-10 my-10 px-10 py-7 rounded-lg w-full"},["success"===t.icon?e("img",{staticClass:"h-14 mb-6 w-14",attrs:{src:s(54398)}}):t._e(),t.title?e("div",{staticClass:"break-words font-bold max-w-xs mb-4 text-xl"},[t._v(t._s(t.title))]):t._e(),t.message?e("div",{staticClass:"break-words leading-5 max-w-xs mb-6 opacity-60 text-base text-center text-dark-message"},[t._v(" "+t._s(t.message)+" ")]):t._e(),e("primary-button",{staticClass:"mt-2",attrs:{title:t.action},on:{click:t.runActionAndClose}})],1)])])},n=[],a=s(25319),l={name:"AlertDialog",components:{PrimaryButton:a.Z},props:{icon:{default:"",type:String}},data(){return{action:"",callback:null,message:"",showing:!1,title:""}},methods:{async runActionAndClose(){this.callback&&await this.callback(),this.showing=!1},show(t,e,s,i){this.title=t,this.message=e,this.showing=!0,this.action=s||this.$t("general.dismiss"),this.callback=i}}},o=l,r=s(1001),c=(0,r.Z)(o,i,n,!1,null,"6503e9d2",null),d=c.exports},210:function(t,e,s){s.d(e,{Z:function(){return c}});s(57658);var i=function(){var t=this,e=t._self._c;return e("div",{staticClass:"active:brightness-75 flex flex-row h-14 items-center px-4 py-2",on:{click:function(e){t.to?t.$router.push(t.to):t.$emit("click")}}},[e("div",{staticClass:"mr-4 w-4"},[t.icon?e("img",{staticClass:"me-4 text-2xl text-primary-100",attrs:{src:t.icon}}):t._e()]),e("div",[e("div",[t._v(t._s(t.title))]),t.subtitle?e("div",{staticClass:"text-xs",class:t.subtitleClass},[t._v(t._s(t.subtitle))]):t._e()]),e("div",{attrs:{ckass:"flex-grow"}}),t.loading?e("i",{staticClass:"animate-spin icon-spinner"}):t.appendIcon?e("i",{staticClass:"se-4 text-2xl text-primary-100",class:t.appendIcon}):t._e()])},n=[],a={name:"ListItem",components:{},props:{appendIcon:{default:"",type:String},icon:{default:"",type:String},loading:{type:Boolean},subtitle:{default:"",type:String},subtitleClass:{default:"",type:String},title:{default:"",type:String},to:{default:"",type:String}}},l=a,o=s(1001),r=(0,o.Z)(l,i,n,!1,null,null,null),c=r.exports},82403:function(t,e,s){s.d(e,{Z:function(){return c}});var i=function(){var t=this,e=t._self._c;return e("div",{staticClass:"flex items-center justify-center relative"},[e("input",{staticClass:"absolute appearance-none bg-white block border-4 h-6 rounded-full toggle-checkbox w-6",class:t.disabled?"cursor-not-allowed":"cursor-pointer",attrs:{name:"toggle",type:"checkbox"},domProps:{checked:t.checked}}),e("label",{staticClass:"flex h-6 relative select-none w-12",class:t.disabled?"cursor-not-allowed":"cursor-pointer",attrs:{for:"toggle"}},[e("span",{staticClass:"absolute h-full left-0 rounded-full top-0 w-full",class:{"bg-accent":t.checked,"bg-dark-N20":!t.checked}}),e("span",{staticClass:"absolute bg-white border-2 duration-300 ease-in-out flex h-6 items-center justify-center rounded-full transition-transform w-6",class:{"right-0":t.checked,"border-accent":t.checked,"border-dark-N20":!t.checked}})])])},n=[],a={name:"OperaToggle",props:{checked:{default:!1,type:Boolean},disabled:{default:!1,type:Boolean}}},l=a,o=s(1001),r=(0,o.Z)(l,i,n,!1,null,null,null),c=r.exports},58448:function(t,e,s){s.d(e,{Z:function(){return c}});var i=function(){var t=this,e=t._self._c;return e("div",[e("transition",{attrs:{name:"fade"}},[t.showing?e("div",{staticClass:"bg-black bottom-0 fade fixed left-0 opacity-60 px-4 right-0 top-0 z-50",on:{click:t.close}}):t._e()]),e("transition",{attrs:{name:"slide"}},[t.showing?e("div",{staticClass:"-translate-x-1/2 bg-modal bottom-0 fixed left-1/2 max-h-screen max-w-screen-sm overflow-y-scroll p-4 rounded-t-3xl w-screen z-50"},[t._t("default")],2):t._e()])],1)},n=[],a={name:"BottomSheet",data(){return{showing:!1}},methods:{close(){this.$emit("close"),this.showing=!1},show(){this.showing=!0}}},l=a,o=s(1001),r=(0,o.Z)(l,i,n,!1,null,"70f89c6e",null),c=r.exports},16701:function(t,e,s){s.d(e,{Z:function(){return h}});var i=function(){var t=this,e=t._self._c;return e("bottom-sheet",{ref:"sheet"},[e("div",[t.title?e("div",{staticClass:"font-bold mb-2 text-xl"},[t._v(" "+t._s(t.title)+" ")]):t._e(),t._l(t.items,(function(s){return e("div",{key:s.key,on:{click:function(e){return t.itemClicked(s.key)}}},["listItem"===s.type?e("list-item",{staticClass:"-mx-4",attrs:{"append-icon":s.appendIcon,icon:s.icon,loading:s.loading,subtitle:s.subtitle,"subtitle-class":s.subtitleClass,title:s.title},on:{click:function(e){return t.itemClicked(s.key)}}}):t._e(),"divider"===s.type?e("div",{staticClass:"border-positive-10 border-t my-2"}):t._e()],1)}))],2)])},n=[],a=s(58448),l=s(210),o={name:"ListSheet",components:{BottomSheet:a.Z,ListItem:l.Z},data(){return{action:null,items:null,onItemClicked:null,title:null}},methods:{itemClicked(t){this.onItemClicked&&this.onItemClicked(t),this.$refs.sheet.close()},show(t,e=[],s,i){this.title=t,this.items=e,this.onItemClicked=s,this.action=i,this.$refs.sheet.show()}}},r=o,c=s(1001),d=(0,c.Z)(r,i,n,!1,null,null,null),h=d.exports},4800:function(t,e,s){s.r(e),s.d(e,{default:function(){return k}});var i=function(){var t=this,e=t._self._c;return e("div",{staticClass:"flex flex-col"},[e("top-bar",{attrs:{"back-override":t.backOverride,title:t.$t("general.fioHandle")}}),e("div",{staticClass:"flex flex-col flex-grow items-center px-8 py-8"},[e("div",{staticClass:"bg-n3 flex flex-row items-center p-4 rounded-lg w-full"},[e("img",{staticClass:"h-10 w-10",attrs:{src:s(81741)}}),e("div",{staticClass:"font-bold ms-2 text-center text-emphasis-high text-md"},[t._v(" "+t._s(t.handle)+" ")]),e("div",{staticClass:"flex-grow"})]),e("div",{staticClass:"flex flex-col mt-4 w-full",class:{"pointer-events-none animate-pulse":t.isLoading}},t._l(t.connections,(function(s,i){return e("div",{key:s.symbol,staticClass:"bg-n2 cursor-pointer flex items-center justify-between mb-2 px-4 py-3 rounded-lg",on:{click:function(e){return t.toggle(i)}}},[e("token-icon",{staticClass:"h-10 object-contain rounded-full w-10",attrs:{address:t.nullAddress,chain:t.connection2chain(s)}}),e("div",{staticClass:"flex-1 mx-4"},[e("div",[t._v(t._s(s.name))]),e("div",{staticClass:"text-emphasis-medium text-xs"},[t._v(t._s(i))])]),e("opera-toggle",{class:`t-fio-${i}-switch`,attrs:{checked:t.checked(i)}})],1)})),0),e("alert-dialog",{ref:"errorDialog"}),e("list-sheet",{ref:"handleSheet"}),e("div",{staticClass:"flex-grow"}),e("div",{staticClass:"mt-5"},[e("div",{staticClass:"flex-col p-4"},[e("div",{staticClass:"font-bold leading-5 mb-8 mx-8 text-dark-N77 text-sm",class:{"opacity-0":!t.changes.dirty}},[t._v(" "+t._s(t.$t("fio.changesNeedConfirmation"))+" ")]),e("primary-button",{staticClass:"flex-1 w-full",attrs:{disabled:!t.changes.dirty,loading:t.isLoading,title:t.$t("general.save")},on:{click:t.save}})],1)])],1)],1)},n=[],a=(s(57658),s(84924)),l=s(47812),o=s(66229),r=s(90881),c=s(16701),d=s(82403),h=s(25319),u=s(69790),f=s(92266),m=s(69986),g=s(88498),p=s(25108),b={name:"FioConnect",components:{AlertDialog:r.Z,ListSheet:c.Z,OperaToggle:d.Z,PrimaryButton:h.Z,TokenIcon:f.Z,TopBar:m.Z},data(){return{backOverride:this.$route.params?.backOverride,connections:a.T_,handle:"",handles:[],nullAddress:l.L1,selected:{}}},computed:{changes(){const{selected:t}=this,e=this.original(),s=Object.values(e).filter((e=>!t[e.chainCode])),i=Object.values(t).filter((t=>!e[t.chainCode]));return{additions:i,dirty:s.length||i.length,removals:s}},connectable(){const t=this.$store.getters.fioConnectableAddresses,e={};if(t?.length)for(const s of t)e[s.chainCode]=s;return e},connection2chain(){return t=>(0,o.aP)(t.chainUId)},isLoading(){return this.$store.getters.isLoading("fio")}},watch:{handle:{handler(t){this.fetchAllPublicAddressesByHandle(t)}}},async mounted(){u.Z.sendStatsEvent(u.Z.types.IMPRESSION,"wt_setting_fio"),this.handle=this.$route.query.handle,await this.$store.dispatch("getFioConnectableAddresses"),await this.$store.dispatch("fetchFioHandles")},methods:{checked(t){return!!this.selected[t]},async fetchAllPublicAddressesByHandle(t){await this.$store.dispatch("fetchAllPublicAddressesByHandle",t),this.selected={...this.original()}},original(){const{connectable:t}=this,e=this.$store.getters.allPublicAddressesByHandle(this.handle),s={};if(e.length)for(const i of e)s[i.chain_code]={address:i.public_address||t[i.chain_code]?.address,chainCode:i.chain_code};return s},async save(){await this.untilLoaded(),this.$store.commit("START_LOADING",{fio:"addressLedgerUpdate"}),this.$authenticator.lockAuthenticatorWithPassword();try{this.changes.additions.length>0&&await g.Z.fioAddAddresses(this.$store.getters.fioPublicKey,this.handle,this.changes.additions),this.changes.removals.length>0&&await g.Z.fioRemoveAddresses(this.$store.getters.fioPublicKey,this.handle,this.changes.removals)}catch(t){p.error("ERROR SAVING FIO CHANGES",t),this.$errorReporter.reportError(t)}this.$authenticator.clearSecretAndUnlockAuthenticator(),await this.fetchAllPublicAddressesByHandle(this.handle),this.$store.commit("FINISH_LOADING",{fio:"addressLedgerUpdate"})},showErrorDialog(){this.$refs.errorDialog.show(this.$t("errors.generic.oops"),this.$t("errors.generic.somethingWentWrong"),null,(()=>this.$router.replace("/settings")))},showHandleSheet(){if(this.isLoading)return;const t=this.$store.getters.fioHandles,e=t.map((t=>({appendIcon:this.handle===t?"icon-checkmark":null,key:t,title:t,type:"listItem"})));e.push({type:"divider"}),e.push({icon:"icon-plus",key:"action",title:this.$t("fio.register.createHandle"),type:"listItem"}),this.$refs.handleSheet.show(this.$t("fio.chooseActiveHandle"),e,(e=>{"action"===e?this.$router.push({name:"FioRegister",query:{hasOperaDomain:t.some((t=>t.endsWith("@opera"))).toString()}}):this.handle=e}))},async toggle(t){const e=this.selected[t];e?this.$delete(this.selected,t):this.$set(this.selected,t,{address:this.connectable[t].address,chainCode:t})},untilLoaded(){const t=e=>{this.isLoading?setTimeout((()=>t(e)),100):e()};return new Promise((e=>{t(e)}))}}},v=b,x=s(1001),w=(0,x.Z)(v,i,n,!1,null,null,null),k=w.exports},81741:function(t,e,s){t.exports=s.p+"img/fio.82458516.svg"}}]);