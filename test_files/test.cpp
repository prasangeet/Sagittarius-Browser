#include <bits/stdc++.h>
// #include <ostream>
// #include <vector>

using namespace std;

struct ListNode {
  int val;
  ListNode* next;
  ListNode(): val(0), next(nullptr) {}
  ListNode(int x): val(x), next(nullptr) {}
  ListNode(int x, ListNode* nxt): val(x), next(nxt) {}
};

class Solution {
public:
  ListNode* merge(ListNode* l1, ListNode* l2){
    ListNode dummy(0);
    ListNode* tail = &dummy;

    while (l1 && l2) {
      if(l1->val < l2->val){
        tail->next = l1;
        l1 = l1->next;
      } else {
        tail->next = l2;
        l2 = l2->next;
      }
      tail = tail->next;
    }

    tail->next = (l1 ? l1 : l2);
    return dummy.next;
  }

  ListNode* sortList(ListNode* head){
    if(!head || !head->next) return head;
    ListNode* fast = head;
    ListNode* slow = head;

    while (fast->next && fast->next->next) {
      fast = fast->next->next;
      slow = slow->next;
    }
    
    ListNode* head2 = slow->next;
    slow->next = nullptr;

    ListNode* left = sortList(head);
    ListNode* right = sortList(head2);

    return merge(left, right);
  }
};

int main(){
  ListNode* head = new ListNode(5);
  head->next = new ListNode(3);
  head->next->next = new ListNode(4);
  head->next->next->next = new ListNode(2);

  Solution sol;
  ListNode* sorted = sol.sortList(head);

  ListNode* curr = sorted;
  while (curr) {
    cout<<curr->val<<"->";
    curr = curr->next;
  }
  cout<<"NULL"<<endl;
}
