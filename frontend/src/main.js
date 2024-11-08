// import 'bootstrap/dist/css/bootstrap-grid.min.css';

import { createApp, reactive } from 'vue';
import App from './App.vue';
import router from './router';
import store from './store';

// PrimeVue
// import 'primevue/resources/themes/lara-dark-green/theme.css';
// import 'primevue/resources/primevue.min.css';
// import 'primeicons/primeicons.css';
import PrimeVue from 'primevue/config';
import './assets/main.scss';
import Aura from '@primevue/themes/aura';
import 'primeicons/primeicons.css';
import ConfirmationService from 'primevue/confirmationservice';

import Button from 'primevue/button';
import InputText from 'primevue/inputtext';
import FloatLabel from 'primevue/floatlabel';
import Textarea from 'primevue/textarea';
import Toast from "primevue/toast";
import ToastService from "primevue/toastservice";
import IconField from 'primevue/iconfield';
import InputIcon from 'primevue/inputicon';
import Avatar from 'primevue/avatar';
import FileUpload from 'primevue/fileupload';
import Menu from 'primevue/menu';
import Toolbar from 'primevue/toolbar';
import Splitter from 'primevue/splitter';
import SplitterPanel from 'primevue/splitterpanel';
import Chip from 'primevue/chip';
import Menubar from 'primevue/menubar';
import Card from 'primevue/card';
import DatePicker from 'primevue/datepicker';
import ProgressSpinner from 'primevue/progressspinner';
import Skeleton from 'primevue/skeleton';
import ScrollPanel from 'primevue/scrollpanel';
import ScrollTop from "primevue/scrolltop";
import Select from 'primevue/select';
import MultiSelect from 'primevue/multiselect';
import VirtualScroller from "primevue/virtualscroller";


import Ripple from "primevue/ripple";
import Column from "primevue/column";
import DataTable from "primevue/datatable";
import TreeTable from 'primevue/treetable';
import ConfirmDialog from "primevue/confirmdialog";
import PanelMenu from 'primevue/panelmenu';
import Badge from 'primevue/badge';
import BadgeDirective from 'primevue/badgedirective';
import Dialog from 'primevue/dialog';
import DynamicDialog from 'primevue/dynamicdialog';
import DialogService from "primevue/dialogservice";
import Rating from 'primevue/rating';
import InputNumber from 'primevue/inputnumber';

// Global axios defaults
// axios.defaults.withCredentials = true;
// axios.defaults.baseURL = 'http://yourapi.domain.com'; // Change to your API's base URL

const app = createApp(App);

const globalState = reactive({
    title: 'AYA'
});

app.provide('globalState', globalState);
app.use(store);
app.use(router);

app.use(PrimeVue, {
    theme: {
        preset: Aura,
        options: {
            darkModeSelector: '.tg-miniapp-dark',
        }
    }
});

app.use(ToastService);
app.use(ConfirmationService);
app.use(DialogService);

app.directive('ripple', Ripple);
app.directive('badge', BadgeDirective);

app.component('Button', Button);
app.component('InputText', InputText);
app.component('FloatLabel', FloatLabel);
app.component('Textarea', Textarea);
app.component('Toast', Toast);
app.component('IconField', IconField);
app.component('InputIcon', InputIcon);
app.component('Avatar', Avatar);
app.component('FileUpload', FileUpload);
app.component('Menu', Menu);
app.component('Toolbar', Toolbar);
app.component('Splitter', Splitter);
app.component('SplitterPanel', SplitterPanel);
app.component('Chip', Chip);
app.component('Menubar', Menubar);
app.component('Card', Card);
app.component('DatePicker', DatePicker);
app.component('ProgressSpinner', ProgressSpinner);
app.component('Skeleton', Skeleton);
app.component('ScrollPanel', ScrollPanel);
app.component('VirtualScroller', VirtualScroller);
app.component('ScrollTop', ScrollTop);
app.component('Select', Select);
app.component('MultiSelect', MultiSelect);
app.component('Column', Column);
app.component('DataTable', DataTable);
app.component('TreeTable', TreeTable);
app.component('ConfirmDialog', ConfirmDialog);
app.component('PanelMenu', PanelMenu);
app.component('Badge', Badge);
app.component('DynamicDialog', DynamicDialog);
app.component('Dialog', Dialog);
app.component('Rating', Rating);
app.component('InputNumber', InputNumber);

app.mount('#app');
