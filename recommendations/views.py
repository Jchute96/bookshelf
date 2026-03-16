from django.shortcuts import render
from .models import Recommendation
from .services import generate_recommendations
from django.contrib.auth.decorators import login_required


@login_required
def my_recommendations(request):
    
    user = request.user
    not_enough_books = False
    
    # Get all recommendations that belong to the current user
    recommendations = Recommendation.objects.filter(user=user) 
    
    # If there are no recommendations saved for the user, generate them
    if not recommendations:
        
        recommendations = generate_recommendations(user)
        
        # If there are no recommendations generated that means user did not have enough finished books
        if not recommendations:
            
            # Set flag to display message in template for user to finish and add more books to get recommendations
            not_enough_books = True
        
        # Else save the newly generated recommendations as Recommendation objects  
        else:
            for recommendation in recommendations:
            
                Recommendation.objects.create(
                    user=user,
                    title=recommendation['title'],
                    author=recommendation['authors'],
                    cover_link=recommendation['image'],
                    purchase_link=recommendation['purchase_link'],
                    reason=f"Because you enjoy books by {recommendation['searched_author']}"  
                )
            
            # Get the newly created recommendations for the user
            recommendations = Recommendation.objects.filter(user=user)
            
    context = {'recommendations': recommendations, 'not_enough_books': not_enough_books}
    return render(request, 'recommendations/my-recommendations.html', context)

    
        
    
    
    
    
    
