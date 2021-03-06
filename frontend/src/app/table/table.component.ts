import { Component, OnInit, ViewChild, ElementRef } from '@angular/core';
import {ApiService} from '../api.service';
import {Observable} from 'rxjs/Rx';
import 'rxjs/add/operator/map';
import 'rxjs/add/operator/catch';
import {DataTableModule, SharedModule, DropdownModule, SelectItem, BlockUIModule, ButtonModule, InputTextModule} from 'primeng/primeng';

@Component({
  selector: 'app-table',
  templateUrl: './table.component.html',
  styleUrls: ['./table.component.css']
})
export class TableComponent implements OnInit {
	
	//general data
	public allTags; //used in getTags 
	public tagData; //used in getTagData 
	rows = []; //rows for main table

	//used to pass expanded row name to getTagData (load tag info on expand)
	eventData = {};

	//filter options
	selectCategory: SelectItem[];
	categoryTemp: string[];
	selectIntention: SelectItem[];
	intentionTemp: string[];
	confidenceOptions: any[] = []

	//loading 
	loading: boolean;
	loadingDetail: boolean;
	blocked: boolean = false;

	constructor(private _apiService: ApiService) {}

	ngOnInit() {
		//subcribe to getTags and create filters for columns
		//
		this.getTags().subscribe(_ => {;
			this.loading = false; //stop loading icon
			
			//category filter options (get all categories)
			this.selectCategory = [];

			//set All to no filter
			this.selectCategory.push({label: 'All', value: null});

			//map categories from allTags (get all categories)
			const categories = this.allTags.tags.map(data => data.category);

			//filter out duplicate categories
			this.categoryTemp = categories.filter((x, i, a) => x && a.indexOf(x) === i);

			//push categories into selectItems to show category filters
			for(let category of this.categoryTemp){
				this.selectCategory.push({label: category, value: category});
			}

			//intention filter options (get all intention options)
			this.selectIntention = [];

			//set All to no filter
			this.selectIntention.push({label: 'All', value: null});

			//map intentions from allTags (get all intentions)
			const intentions = this.allTags.tags.map(data => data.intention);

			//filter out duplicate intentions
			this.intentionTemp = intentions.filter((x, i, a) => x && a.indexOf(x) === i);

			//push intentions into selectIntention to show intention filters
			for(let intention of this.intentionTemp){
				this.selectIntention.push({label: intention, value: intention});
			}

    	});    	

		//set confidence filter options (static because only three options (change?))
		this.confidenceOptions.push({label: 'All', value: null});
		this.confidenceOptions.push({label: 'high', value: 'high'});
		this.confidenceOptions.push({label: 'medium', value: 'medium'});
		this.confidenceOptions.push({label: 'low', value: 'low'});
	}
	//get tag information for main table (name, category, intention, and confidence)
	getTags(){
		this.loading = true
		return this._apiService
			.getTags()
			.map(
				(data) => {
					this.allTags = data;
					this.rows = this.allTags.tags;
			})
			.catch((error) => {
				throw error;
			});
	}
	//called when row is expanded and then subscribe to getTagData to get information on tag selected
	loadTagInstances(event){
		this.getTagData(event.data['name']).subscribe(_ => {;
			this.loadingDetail = false;
    		this.eventData[event.data['name']] = this.tagData.records 
    	});
	}
	//gets all tag instances (IPs and dates) for a specific tag 
	getTagData(tagName: string){
		this.loadingDetail = true
		return this._apiService
			.getTagData(tagName)
			.map(
				(data) => {
					this.tagData = data;
			})
			.catch((error) => {
				throw error;
			});
	}

}
