def create_user_subscription(user_id):
    user = UserProfile.objects.get(id=user_id)
    spg = PaymentDetails.objects.filter(	user=user).last().cart.sellable_product_group
    payment = PaymentDetails.objects.filter(user=user, cart__sellable_product_group=spg).last()
    completed_on = payment.completed_on
    plan_end_date = completed_on + datetime.timedelta(days=spg.duration)
    status = 1
    added_on = completed_on
    updated_on = completed_on
    UserSubscription.objects.create(user=user, sellable_product_group=spg, payment=payment, status=1, plan_end_date=plan_end_date, added_on=completed_on, updated_on=completed_on)
    print("created")
UserSubscription.objects.create(user=user, sellable_product_group=spg, payment=payment, status=1, plan_end_date=plan_end_date, added_on=completed_on, updated_on=completed_on)

def get_session(sessionId):
    from django.contrib.sessions.models import Session
    session = Session.objects.get(session_key=sessionId)
    session_data = session.get_decoded()
    user = session_data.get('_auth_user_id')
    print(user)


local shell plus =>
curl --location --request DELETE 'https://elasticsearch.careers360.de/qna'
es = Elasticsearch('https://elasticsearch.careers360.de/')
es.indices.create(index="qna")

on server =>
python3 manage.py index_qna_documents_elastic