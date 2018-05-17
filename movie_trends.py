'''
importing the required modules and the apikey
'''
from apikeys import TMDB_KEY
import requests
import bokeh
from bokeh.io import show, output_file
from bokeh.models import ColumnDataSource, FactorRange
from bokeh.plotting import figure
import time


def first_anlaysis():
    def genre_connection(TMDB_KEY):
        payload={"api_key":TMDB_KEY}
        genre_list= requests.get("https://api.themoviedb.org/3/genre/movie/list?", params=payload)
        return genre_list.json()

    answer=genre_connection(TMDB_KEY)

mylist=[]
master_dict={}

def first_function(genreid,genre,apival,monthname):
    '''using request.get method calling the api and fetching the result and appending it to a list
    '''
    movie_list=requests.get("http://api.themoviedb.org/3/discover/movie?api_key=7501e3ab4ad65ae81ad0b0dd10b1813d&with_genres="+ str(genreid)+apival)
    
    movie=movie_list.json()
    mylist.append(movie['total_results'])
    
    return mylist

def first_subFunction():
    '''
    passing monthname,genres and apival to the first_function and then computing a dictionary that stores the required values 
    that needs to be plot
    '''

    genresdict={"A":28, 'D': 99, "C":35,"Cr":80,"Dr":18}
    
    month_dict={'jan':"&primary_release_date.gte=2016-01-01&primary_release_date.lte=2016-01-31","feb":"&primary_release_date.gte=2016-02-01&primary_release_date.lte=2016-02-28","march":"&primary_release_date.gte=2016-03-01&primary_release_date.lte=2016-03-31","april":"&primary_release_date.gte=2016-04-01&primary_release_date.lte=2016-04-30","may":"&primary_release_date.gte=2016-05-01&primary_release_date.lte=2016-05-31","june":"&primary_release_date.gte=2016-06-01&primary_release_date.lte=2016-06-30","july":"&primary_release_date.gte=2016-07-01&primary_release_date.lte=2016-07-31","august":"&primary_release_date.gte=2016-07-01&primary_release_date.lte=2016-07-31","september":"&primary_release_date.gte=2016-09-01&primary_release_date.lte=2016-09-30","october":"&primary_release_date.gte=2016-10-01&primary_release_date.lte=2016-10-31","november":"&primary_release_date.gte=2016-11-01&primary_release_date.lte=2016-11-30","december":"&primary_release_date.gte=2016-12-01&primary_release_date.lte=2016-12-31"}  
    for genre,genreid in genresdict.items():
        time.sleep(10)
        print(".....")
        for monthname,apival in month_dict.items():
            
            
           
          f=first_function(genreid,genre,apival,monthname)
          
  
    i=0
    for genre, genreid in genresdict.items():
        master_dict[genre]=[]
        for monthname,apival in month_dict.items():
            master_dict[genre].append(mylist[i])
            i+=1
    return master_dict

def viz(get_master):
    '''
    This function buiods the viz with the necessary labels and values that it received from the first_subfunction
    '''
    genres = ['A', 'D', 'C', 'Cr', 'Dr']
    months = ['Jan', 'feb',"march","april","may","june","july","august","septmeber","october","november","december"]
    data = get_master
    x = [ (month, genre) for month in months for genre in genres ]
    '''
    aggregating the data for each genre pertaining to each month
    '''
    output_file("genre_by_season.html")
    counts = sum(zip(data['A'], data['D'], data['C'], data['Cr'], data['Dr']), ())
    source = ColumnDataSource(data=dict(x=x, counts=counts))
    p = figure(x_range=FactorRange(*x), plot_height=250,plot_width=1000, title=" By month",
           toolbar_location=None, tools="")
    p.vbar(x='x', top='counts', width=0.3, source=source)
    return show(p)
       

def pop_actors(get_id, TMDB_KEY, name):
    '''computing the url with the necessary uri and query parameters used tofetch the actos and his popularity
    '''
    resource_uri = 'https://api.themoviedb.org/3/person/' + str(get_id) + '/movie_credits'
    query_params = {'api_key': TMDB_KEY, 'sort_by': 'release_date.asc'}
    #https://api.themoviedb.org/3/discover/movie?api_key=9e97ac7a211a470e646551c486060949&language=en-US&sort_by=popularity.desc&include_adult=false&include_video=false&page=1&with_cast=11701
    response = requests.get(resource_uri, params = query_params)
    test = response.json()
    
    '''
    computing the total popularity of that particular actor in each month
    '''
    pop_dict = {}
    for c in test['cast']:
        if 'release_date' in c and c['release_date'] != '' and c['release_date'] < '2018-01-01':
            release_date = c['release_date'].split('-')
            if release_date[0] in list(pop_dict.keys()):
                pop_dict[release_date[0]] += c['popularity']
            else:
                pop_dict[release_date[0]] = c['popularity']
    '''
    outputing the html file
    '''
    output_file("actor_popularity.html")

    p = figure(title=f"Popularity of {name}", plot_width=400, plot_height=400)

    '''
    drawing the line chart
    '''
    p.line(sorted(list(pop_dict.keys())), sorted(list(pop_dict.values())), line_width=2)

    show(p) 
        
def main():
    '''
    asking the user to input the name of the actor whose popularity he or she wishes to analyze
    '''
    askUser = int(input('Which of the two analysis do you want to run? Choose either 1 or 2: '))
    if askUser == 1:
        get_master = first_subFunction()
        call = viz(get_master)
   
    elif askUser == 2:
        name = input('Which actor do you wanna search?')
        resource_uri = "https://api.themoviedb.org/3/search/person?"
        query_params = { 'query': name,'api_key': TMDB_KEY}
        response = requests.get(resource_uri, params = query_params)
        test = response.json()
        '''
        if name is incorrect it againn asks the user to enter the correct name
        '''
    
        if test['total_results'] > 0:
            get_id = test['results'][0]['id']
            
            pop_actors(get_id,TMDB_KEY, name)
        else:
            print('Please enter correct name')
            main()
        
    else:
        print('Please choose a valid number')
'''
calls the main function
'''
if __name__ == '__main__':
    main()